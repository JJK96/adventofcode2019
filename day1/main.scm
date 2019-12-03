(import (chicken io))
(import (chicken format))

(define (mass_to_fuel mass) (- (floor (/ mass 3)) 2))

(define (fuel_usage input) 
    (define usage (mass_to_fuel input))
    (if (< usage 0) 0 (+ usage (fuel_usage usage))))

(define inputs (map string->number (read-lines (open-input-file "input"))))
(printf "1: ~a\n" (apply + (map mass_to_fuel inputs)))
(printf "2: ~a\n" (apply + (map fuel_usage inputs)))
