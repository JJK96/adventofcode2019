(import srfi-1)
(import srfi-13)
(import matchable)
(import (chicken format))
(import (chicken io))
(import (chicken string))
(define (insert value addr memory)
    (define-values (before after) (split-at memory addr))
    (append before (list value) (drop after 1)))

#;(display (insert 4 2 '(1 2 3)))

(define (computer ip memory) 
    (define (update-memory op par1 par2 dest memory)
        (insert (op (list-ref memory par1) (list-ref memory par2)) dest memory))
    (match (take (drop memory ip) 5)
        [(99 _ _ _ _) memory]
        [(1 par1 par2 dest _) (computer (+ ip 4) (update-memory + par1 par2 dest memory))]
        [(2 par1 par2 dest _) (computer (+ ip 4) (update-memory * par1 par2 dest memory))]
        [_ "unknown opcode"]))

(define (compute noun verb input)
    (computer 0 (insert noun 1 (insert verb 2 input))))

(define contents (string-drop-right (read-string 512 (open-input-file "input")) 1))
(define input (map string->number (string-split contents ",")))
(printf "1: ~a\n" (list-ref (compute 12 2 input) 0))
(define (find-noun-verb noun)
    (define find-verb 
        (lambda (verb)
            (if (= (list-ref (compute noun verb input) 0) 19690720)
               verb
               (if (not (= verb 99))
                   (find-verb (+ verb 1))
                   #f))))
    (define verb (find-verb 0))
    (if verb
       (list noun verb)
       (if (not (= noun 99))
           (find-noun-verb (+ noun 1))
           #f)))
(define noun-verb (find-noun-verb 0))
(printf "2: ~a\n" (+ (second noun-verb) (* 100 (first noun-verb))))
