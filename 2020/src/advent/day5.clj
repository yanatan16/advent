(ns advent.day5
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 5)
(def input' (delay (get-lined-input day)))

(defn str->binary [s char-for-1]
  (->> s
       (map #(if (= % char-for-1) 1 0))
       reverse
       (map-indexed #(* (Math/pow 2 %1) %2))
       (apply +)
       int))

(defn row [line]
  (str->binary (take 7 line) \B))

(defn aisle [line]
  (str->binary (drop 7 line) \R))

(def position (juxt row aisle))

(defn seat-id [[row aisle]]
  (+ (* row 8) aisle))

(defn parse [line]
  (let [[row aisle] (position line)]
    {:row row
     :aisle aisle
     :seat-id (seat-id [row aisle])}))

(assert (= [70 7] (position "BFFFBBFRRR")))
(assert (= [14 7] (position "FFFBBBFRRR")))
(assert (= [102 4] (position "BBFFBBFRLL")))

(defn solve-part-1 [input]
  (p* day 1
      (->> input
           (map parse)
           (map :seat-id)
           (apply max))))

(defn solve-part-2 [input]
  (p* day 2
      (let [ids (->> input
                     (map parse)
                     (map :seat-id))
            min-id (apply min ids)
            max-id (apply max ids)]
        (-> (set (range min-id max-id))
            (set/difference (set ids))
            first))))

(comment
  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
