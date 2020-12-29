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
  (->> starting
       (map-indexed vector)
       butlast
       (reduce (fn [state [i v]] (assoc state v (- (+ 1 i) (count starting)))) {})))

(defn next-turn [state last-turn]
  (if-let [last-spoken (get state last-turn)]
    (- last-spoken)
    0))

(defn dec-state [state]
  (reduce-kv #(assoc %1 %2 (dec %3)) {} state))

(declare step-memo)

(defn step [state last-turn]
  (let [next-state (dec-state (assoc state last-turn 0))
        turn (next-turn state last-turn)]
    #_(println :step state last-turn)
    (lazy-cat (list turn)
              (step-memo next-state turn))))

(def step-memo (memoize step))

(defn run [starting]
  (lazy-cat
   starting
   (step-memo (starting->state starting) (last starting))))

(defn run-until [starting until]
  (->> (run starting)
       (drop (dec until))
       first))

(defn solve-part-1 [starting]
  (p* day 1
      (run-until starting 2020)))

;; FIXME This takes too long; memoization kills heap space. Not sure how to solve this.
(defn solve-part-2 [starting]
  (p* day 2
      (run-until starting 30000000)))

(comment
  (take 10 (run [0 3 6]))

  (run-until [0,3,6] 2020)
  (run-until [1,3,2] 2020)
  (run-until [2 1 3] 2020)

  (run-until [0 3 6] 30000000)


  (do
    (solve-part-1 [1,12,0,20,8,16])

    (solve-part-2 [1,12,0,20,8,16])
    )
  )

(defn -main []
  (solve-part-2 [1,12,0,20,8,16]))
