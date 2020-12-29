(ns advent.day17
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 17)
(def input' (delay (get-lined-input day)))

(defn iteratedly [n f state]
  (loop [n n state state]
    (if (zero? n)
      state
      (recur (dec n) (f state)))))

(def example-input (str/split-lines ".#.
..#
###"))

(defn pt1-parse [input]
  [(vec (map vec input))])

(defn pt1-count-active [state]
  (->> state
       (apply concat)
       (apply concat)
       (filter #(= % \#))
       count))

(defn pt1-active? [state x y z]
  (= \# (get-in state [z y x])))

(defn pt1-count-active-around [state x y z]
  (->> (for [x' [(dec x) x (inc x)]
             y' [(dec y) y (inc y)]
             z' [(dec z) z (inc z)]
             :when (not= [x y z] [x' y' z'])]
         (if (pt1-active? state x' y' z') 1 0))
       (apply +)))

(defn pt1-conway-cube-iteration [state]
  (vec
   (for [z (range -1 (inc (count state)))]
     (vec
      (for [y (range -1 (inc (count (first state))))]
        (vec
         (for [x (range -1 (inc (count (first (first state)))))]
           (case (pt1-count-active-around state x y z)
             3 \#
             2 (if (pt1-active? state x y z) \# \.)
             \.))))))))

(defn solve-part-1 [input]
  (p* day 1
      (pt1-count-active (iteratedly 6 pt1-conway-cube-iteration (pt1-parse input)))))

(defn pt2-parse [input]
  [[(vec (map vec input))]])

(defn pt2-count-active [state]
  (->> state
       (apply concat)
       (apply concat)
       (apply concat)
       (filter #(= % \#))
       count))

(defn pt2-active? [state x y z w]
  (= \# (get-in state [w z y x])))

(defn pt2-count-active-around [state x y z w]
  (->> (for [x' [(dec x) x (inc x)]
             y' [(dec y) y (inc y)]
             z' [(dec z) z (inc z)]
             w' [(dec w) w (inc w)]
             :when (not= [x y z w] [x' y' z' w'])]
         (if (pt2-active? state x' y' z' w') 1 0))
       (apply +)))

(defn pt2-conway-cube-iteration [state]
  (vec
   (for [w (range -1 (inc (count state)))]
     (vec
      (for [z (range -1 (inc (count (first state))))]
        (vec
         (for [y (range -1 (inc (count (first (first state)))))]
           (vec
            (for [x (range -1 (inc (count (first (first (first state))))))]
              (case (pt2-count-active-around state x y z w)
                3 \#
                2 (if (pt2-active? state x y z w) \# \.)
                \.))))))))))

(defn solve-part-2 [input]
  (p* day 2
      (pt2-count-active (iteratedly 6 pt2-conway-cube-iteration (pt2-parse input)))))


(comment
  (-> example-input
      pt2-parse
      pt2-conway-cube-iteration)

  (solve-part-1 example-input)

  (solve-part-2 example-input)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
