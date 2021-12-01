(ns advent.day1
  (:require [advent.utils :refer :all]))

(def input' (delay (get-input-ints 1)))

(defn solve-part-1 [input]
  (let [s (set input)]
    (p* 1 1
        (->> input
             (filter #(contains? s (- 2020 %)))
             (map #(* % (- 2020 %)))
             first))))

(defn solve-part-2 [input]
  (let [s (set input)]
    (p* 1 1
        (first
         (for [x input
               y input
               :when (contains? s (- 2020 x y))]
           (* x y (- 2020 x y)))))))

(comment
  (solve-part-1 @input')

  (solve-part-2 @input')
  )
