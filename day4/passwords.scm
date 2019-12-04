(import list-comprehensions)
(import (chicken format))

(define (number->list num)
  (let loop ((num num)
             (acc '()))
    (if (< num 10)
        (cons num acc)
        (loop (quotient num 10)
              (cons (remainder num 10) acc)))))

(define (adjacent pass last-matched)
    (if (<= (length pass) 1)
        #f
        (or 
         (and
          (= (car pass) (car (cdr pass)))
          (if (>= (length pass) 3)
            (not (= (car (cdr pass)) (car (cdr (cdr pass)))))
            #t)
          (not last-matched))
         (adjacent (cdr pass) (= (car pass) (car (cdr pass)))))))

(define (never-decrease pass)
    (if (<= (length pass) 1)
        #t
        (and
         (<= (car pass) (car (cdr pass)))
         (never-decrease (cdr pass)))))

(define (checks pass)
    (define pass-list (number->list pass))
    (and
     (= 6 (length pass-list))
     (adjacent pass-list #f)
     (never-decrease pass-list)))

(define passes (collect pass (pass (range 153517 630395) (checks pass))))
(printf "1: ~a\n" (length passes))
