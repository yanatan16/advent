(ns advent.day2
  (:require [advent.utils :refer :all]
            [clojure.string :as str]))

(def input' (delay (get-lined-input 2)))

(defprotocol InPolicy
  (in-policy-part1? [this password])
  (in-policy-part2? [this password]))
(defrecord Policy [lower upper letter]
  InPolicy
  (in-policy-part1? [_ password]
    (<= lower (count (filter #(= (first letter) %) password)) upper))
  (in-policy-part2? [_ password]
    (let [letter-char (first letter)
          lower-char (nth password (dec lower))
          upper-char (nth password (dec upper))]
      (or (and (= letter-char lower-char)
               (not= letter-char upper-char))
          (and (not= letter-char lower-char)
               (= letter-char upper-char))))))

(def rgx #"^(\d+)-(\d+) (\w): (\w+)$")
(defn parse [line]
  (if-let [match (re-find rgx line)]
    (let [[_ lower upper letter password] match]
      [(->Policy (Integer/parseInt lower) (Integer/parseInt upper) letter) password])
    (throw (ex-info "Failed to parse line" {:line line}))))

(defn solve-part-1 [input]
  (->> input
       (map parse)
       (filter (fn [[policy password]] (in-policy-part1? policy password)))
       count))

(defn solve-part-2 [input]
  (->> input
       (map parse)
       (filter (fn [[policy password]] (in-policy-part2? policy password)))
       count))

(comment
  (solve-part-1 @input')

  (solve-part-2 @input')
  )
