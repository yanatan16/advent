(ns advent.day3
  (:require [advent.utils :refer :all]
            [clojure.string :as str]))

(def input' (delay (get-lined-input 3)))

(defn tree? [input right down]
  (let [row (nth input down)
        square (nth row (mod right (count row)))]
    (= square \#)))

(defn slope-positions [rows right-slope down-slope]
  (->> (range (/ rows down-slope))
       (map (fn [i] [(* i right-slope)
                     (* i down-slope)]))))

(defn count-slope [input right-slope down-slope]
  (->> (slope-positions (count input) right-slope down-slope)
       (filter (fn [[right down]] (tree? input right down)))
       count))

(defn solve-part-1 [input]
  (p* 3 1
      (count-slope input 3 1)))

(defn solve-part-2 [input]
  (p* 3 2
      (* (count-slope input 1 1)
         (count-slope input 3 1)
         (count-slope input 5 1)
         (count-slope input 7 1)
         (count-slope input 1 2))))

(comment
  (solve-part-1 @input')

  (solve-part-2 @input')
  )
