(ns advent.day15
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str])
  (:gen-class))

(def day 15)

(defn starting->state
  "Convert starting numbers to state:
  {value: turn-spoken}"
  [starting]
  {:ages (->> starting
              (map-indexed vector)
              butlast
              (reduce (fn [state [i v]] (assoc state v (- (+ 1 i) (count starting)))) {}))
   :last (last starting)})

(defn next-turn [ages last-turn]
  (if-let [last-spoken (get ages last-turn)]
    (- last-spoken)
    0))

(defn dec-ages [ages]
  (reduce-kv #(assoc %1 %2 (dec %3)) {} ages))

(defn step [{:keys [ages last]}]
  {:ages (dec-ages (assoc ages last 0))
   :last (next-turn ages last)})

(defn solve-part-1 [starting]
  (p* day 1
      (:last (iterate-until* step
                             (starting->state starting)
                             (- (inc 2020) (count starting))))))

(defn solve-part-2 [starting]
  (p* day 2
      (:last (iterate-until* step
                             (starting->state starting)
                             (- (inc 30000000) (count starting))))))

(comment
  (take 10 (run [0 3 6]))

  (solve-part-1 [0 3 6])
  (:last (iterate-until* step (starting->state [0,3,6]) 2018))

  (solve-part-2 [0 3 6])


  (do
    (solve-part-1 [1,12,0,20,8,16])

    (solve-part-2 [1,12,0,20,8,16])
    )
  )

(defn -main []
  (solve-part-2 [1,12,0,20,8,16]))
