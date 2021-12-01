(ns advent.day9
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 9)
(def input' (delay (get-input-longs day)))

(def example-input [35 20 15 25 47 40 62 55 65 95 102 117 150 182 127 219 299 277 309 576])

(defn xmas-valid?
  ([preamble n] (xmas-valid? preamble n (set preamble)))
  ([preamble n preamble-set]
   (->> preamble
        (filter #(and (not= % (- n %))
                      (contains? preamble-set (- n %))))
        not-empty
        some?)))

(defn find-first-invalid [ns preamble-length]
  (loop [preamble (take preamble-length ns)
         preamble-set (set (take preamble-length ns))
         [next-n & rest-ns] (drop preamble-length ns)]
    #_(println :iteration preamble preamble-set next rest)
    (cond
      (nil? next) (throw (ex-info "No invalid numbers" {:next nil}))
      (not (xmas-valid? preamble next-n preamble-set)) next-n
      :else (recur (concat (rest preamble) [next-n])
                   (conj (disj preamble-set (first preamble)) next-n)
                   rest-ns))))

(defn solve-part-1 [input]
  (p* day 1
      (find-first-invalid input 25)))

(defn find-contiguous-sum [input sum]
  (loop [i 0 j 3]
    (let [contiguous-sum (apply + (map #(or (nth input %) 0) (range i j)))]
      (cond
        ;; safety; dont bother counting less than 2 numbers
        (> 2 (- j i)) (recur i (+ i 2))

        ;; error if we go past the end of the input
        (>= j (count input)) (throw (ex-info "exceeded input size" {:i i :j j}))

        ;; on target
        (= sum contiguous-sum)
        (map #(nth input %) (range i j))

        ;; If less, expand segment
        (> sum contiguous-sum) (recur i (inc j))

        ;; If more, move to next integer, reset to size 2
        (< sum contiguous-sum) (recur (inc i) (+ i 2))))))

(defn solve-part-2 [input]
  (p* day 2
      (let [invalid (find-first-invalid input 25)
            contiguous (find-contiguous-sum input invalid)]
        (+ (first contiguous) (last contiguous)))))


(comment
  (find-first-invalid example-input 5)
  (find-contiguous-sum example-input 127)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
