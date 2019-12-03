(import srfi-1)
(import srfi-13)
(import matchable)
(import (chicken format))
(import (chicken io))
(import (chicken string))
(import list-comprehensions)
(import (chicken sort))

(define (decode direction)
    (list (string-take direction 1) (string->number (string-drop direction 1))))

(define (move start direction num)
    (define-values (x y) (apply values start))
    (define new-pos (match direction
                           ["U" (list x (+ y 1))]
                           ["D" (list x (- y 1))]
                           ["L" (list (- x 1) y)]
                           ["R" (list (+ x 1) y)]))
    (define new-num (- num 1))
    (if (= new-num 0)
        (list new-pos)
        (append (list new-pos) (move new-pos direction new-num))))

(define (plot start directions)
    (define direction (decode (first directions)))
    (define-values (dir num) (apply values direction))
    (define positions (move start dir num))
    (define new-directions (drop directions 1))
    (if (= (length new-directions) 0)
        positions
        (append positions (plot (last positions) new-directions))))

(define input (read-string #f (open-input-file "input")))
(define input (map (lambda (input) (string-split input ",")) (string-split input "\n")))
(define first-plot (plot '(0 0) (first input)))
(define second-plot (plot '(0 0) (second input)))
#;(printf "~a\n" first-plot)
#;(printf "~a\n"  second-plot)
(define (lexicographic x)
    (if (eq? x '())
        #f
        (or (apply < (first x)) (and (apply = (first x)) (lexicographic (drop x 1))))))
(define (compare-list a b)
    (lexicographic (zip a b)))
(define (sort-plot plot) (sort (map (lambda (i) (append (list (apply + (map abs i))) i)) plot) compare-list))
(define first-distances (sort-plot first-plot))
(define second-distances (sort-plot second-plot))
(define (list-equal a b)
    (if (eq? a '())
        #t
        (and (= (first a) (first b)) (list-equal (drop a 1) (drop b 1)))))
(define (find-common a b)
    (if (list-equal (first a) (first b))
        (first a)
        (if (compare-list (first a) (first b))
            (find-common (drop a 1) b)
            (find-common a (drop b 1)))))
(printf "1: ~a\n" (first (find-common first-distances second-distances)))
