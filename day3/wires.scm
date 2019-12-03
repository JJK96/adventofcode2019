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

#;(define input "R75,D30,R83,U83,L12,D49,R71,U7,L72
#;U62,R66,U55,R34,D71,R55,D58,R83")
(define input (read-string #f (open-input-file "input")))
(define input (map (lambda (input) (string-split input ",")) (string-split input "\n")))
(define first-plot (plot '(0 0) (first input)))
(define second-plot (plot '(0 0) (second input)))
(printf "~a\n" first-plot)
(printf "~a\n"  second-plot)
(define intersections (lset-intersection (lambda (a b) (list= eq? a b)) first-plot second-plot))
(define distances (sort (map (lambda (i) (apply + (map abs i))) intersections) <))
(printf "1: ~a\n" (first distances))
