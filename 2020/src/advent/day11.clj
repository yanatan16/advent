(ns advent.day11
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 11)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"))

(defn parse [input]
  (vec (map #(vec (map identity %)) input)))

(defn stable? [state1 state2]
  (= state1 state2))

(defn count-occupied-around [state x y]
  (->> (for [x' [(dec x) x (inc x)]
             y' [(dec y) y (inc y)]
             :when (not= [x y] [x' y'])]
         (if (= \# (get-in state [y' x'])) 1 0))
       (apply +)))

(defn count-occupied [state]
  (->> state
       (apply concat)
       (filter #(= \# %))
       count))

(defn iterate-pt1 [state]
  (vec
   (for [y (range (count state))]
     (vec
      (for [x (range (count (first state)))]
        (case (get-in state [y x])
          \. \.
          \L (if (zero? (count-occupied-around state x y)) \# \L)
          \# (if (> 4 (count-occupied-around state x y)) \# \L)))))))

(defn solve-part-1 [input]
  (p* day 1
      (loop [state1 (parse input)]
        (let [state2 (iterate-pt1 state1)]
          #_(println :iteration state1 state2 (= state1 state2))

          (if (= state1 state2)
            (count-occupied state2)
            (recur state2))))))

(defn first-visible-seat [state x y slope-x slope-y]
  (loop [x' (+ x slope-x) y' (+ y slope-y)]
    (case (get-in state [y' x'])
      \. (recur (+ x' slope-x) (+ y' slope-y))
      \# \#
      \L)))

(defn count-occupied-visible [state x y]
  (->> (for [slope-x [-1 0 1]
             slope-y [-1 0 1]
             :when (not= [slope-x slope-y] [0 0])]
         (if (= \# (first-visible-seat state x y slope-x slope-y)) 1 0))
       (apply +)))

(defn iterate-pt2 [state]
  (vec
   (for [y (range (count state))]
     (vec
      (for [x (range (count (first state)))]
        (case (get-in state [y x])
          \. \.
          \L (if (zero? (count-occupied-visible state x y)) \# \L)
          \# (if (> 5 (count-occupied-visible state x y)) \# \L)))))))

(defn solve-part-2 [input]
  (p* day 2
      (loop [state1 (parse input)]
        (let [state2 (iterate-pt2 state1)]
          (if (= state1 state2)
            (count-occupied state2)
            (recur state2))))))

(comment
  (solve-part-1 example-input)

  (solve-part-2 example-input)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
