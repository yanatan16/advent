(ns advent.day6
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 6)
(def input' (delay (get-double-lined-input day)))

(defn pt1-count-answers [input]
  (->> input
       (filter #(and (not= % (first "\n"))
                     (not= % (first " "))))
       set
       count))

(defn solve-part-1 [input]
  (p* day 1
      (->> input
           (map pt1-count-answers)
           (apply +))))

(defn pt2-count-answers [input]
  (->> (str/split input #"\n")
       (map set)
       (apply set/intersection)
       count))

(defn solve-part-2 [input]
  (p* day 2
      (->> input
           (map pt2-count-answers)
           (apply +))))

(comment
  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
