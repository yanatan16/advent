(ns advent.day22
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 22)
(def input' (delay (get-double-lined-input day)))

(def example-input (str/split "Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10" #"\n\n"))

(defn parse [[deck1 deck2]]
  [(map #(Integer/parseInt %) (rest (str/split-lines deck1)))
   (map #(Integer/parseInt %) (rest (str/split-lines deck2)))])

(defn play-pt1 [deck1 deck2]
  (loop [[card1 & deck1] deck1
         [card2 & deck2] deck2]
    (cond
      (nil? card1) (concat [card2] deck2)
      (nil? card2) (concat [card1] deck1)
      (< card1 card2) (recur deck1 (concat deck2 [card2 card1]))
      (> card1 card2) (recur (concat deck1 [card1 card2]) deck2)
      :else (throw (ex-info "unknown state" {:card1 card1 :deck1 deck1
                                             :card2 card2 :deck2 deck2})))))

(defn score [deck]
  (->> deck
       reverse
       (map-indexed #(* (inc %1) %2))
       (apply +)))

(assert (= 306 (score [3 2 10 6 8 5 9 4 7 1])))

(defn solve-part-1 [input]
  (p* day 1
      (let [[deck1 deck2] (parse input)
            winning-deck (play-pt1 deck1 deck2)]
        (score winning-deck))))

(defn play-pt2 [deck1 deck2]
  (loop [all-previous-game-states #{}
         [card1 & deck1 :as state1] deck1
         [card2 & deck2 :as state2] deck2]
    (let [all-previous-game-states' (conj all-previous-game-states [state1 state2])]
      (cond
        (contains? all-previous-game-states [state1 state2]) [1 state1]

        (nil? card1) [2 state2]

        (nil? card2) [1 state1]

        (and (<= card1 (count deck1))
             (<= card2 (count deck2)))
        (let [[winner _] (play-pt2 (take card1 deck1) (take card2 deck2))]
          (recur all-previous-game-states'
                 (if (= winner 1) (concat deck1 [card1 card2]) deck1)
                 (if (= winner 2) (concat deck2 [card2 card1]) deck2)))

        (< card1 card2) (recur all-previous-game-states'
                               deck1
                               (concat deck2 [card2 card1]))

        (> card1 card2) (recur all-previous-game-states'
                               (concat deck1 [card1 card2])
                               deck2)

        :else (throw (ex-info "unknown state" {:card1 card1 :deck1 deck1
                                               :card2 card2 :deck2 deck2}))))))

(defn solve-part-2 [input]
  (p* day 2
      (let [[deck1 deck2] (parse input)
            [_winner winning-deck] (play-pt2 deck1 deck2)]
        (score winning-deck))))


(comment
  (parse example-input)
  (apply play (parse example-input))

  (solve-part-1 example-input)

  (solve-part-2 example-input)

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
