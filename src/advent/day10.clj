(ns advent.day10
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 10)
(def input' (delay (get-input-ints day)))

(def example-input [16 10 15 5 1 11 7 19 6 12 4])

(defn differences [ns]
  (map #(- %1 %2) ns (rest ns)))

(defn solve-part-1 [input]
  (p* day 1
      (let [adapter-joltages (sort input)
            device-joltage (+ 3 (apply max adapter-joltages))
            all-joltages (concat [0] adapter-joltages [device-joltage])
            diffs (differences (reverse all-joltages))
            freqs (frequencies diffs)]
        (* (get freqs 1) (get freqs 3)))))

(defn connectable? [j1 j2]
  (and (number? j1)
       (number? j2)
       (>= 3 (Math/abs (- j2 j1)))))

(defn count-all-arrangements
  "Counts all arrangements in recursive forward dynamic programming style.
  Probably more efficient to do this backwards, as it would save on recursion cost."
  [joltages]
  (let [base (first joltages)
        next-joltages (rest joltages)]
    (if (empty? next-joltages)
      1
      (+ (count-all-arrangements next-joltages)
         (if (and (< 1 (count next-joltages)) (connectable? base (nth next-joltages 1)))
           (count-all-arrangements (drop 1 next-joltages))
           0)
         (if (and (< 2 (count next-joltages)) (connectable? base (nth next-joltages 2)))
           (count-all-arrangements (drop 2 next-joltages))
           0)))))

(assert (= 1 (count-all-arrangements [1])))
(assert (= 1 (count-all-arrangements [1 2])))
(assert (= 2 (count-all-arrangements [1 2 3])))

(defn take-until-3-diff [joltages]
  (loop [taken [] [j & rest-j :as js] joltages]
    (cond
      (nil? j) [taken []]
      (empty? taken) (recur [j] rest-j)
      (= 3 (- j (last taken))) [taken js]
      :else (recur (concat taken [j]) rest-j))))

(defn segment-by-3-diffs
  "Segment the joltages by differences of 3"
  [joltages]
  (if (empty? joltages)
    '()
    (let [[taken rest] (take-until-3-diff joltages)]
      (lazy-cat [taken] (segment-by-3-diffs rest)))))

(defn solve-part-2 [input]
  (p* day 2
      (let [adapter-joltages (sort input)
            device-joltage (+ 3 (apply max adapter-joltages))
            all-joltages (concat [0] adapter-joltages [device-joltage])
            segments (segment-by-3-diffs all-joltages)]
        (->> segments
             (map count-all-arrangements)
             (apply *)))))

(comment
  (differences (reverse (sort example-input)))
  (solve-part-1 example-input)

  (take-until-3-diff (concat [0] (sort example-input) [22]))
  (segment-by-3-diffs (concat [0] (sort example-input) [22]))
  (solve-part-2 example-input)

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
