(ns advent.day13
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 13)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "939
7,13,x,x,59,x,31,19"))

(defn parse [[arrival-time bus-schedule]]
  {:arrival-time (Integer/parseInt arrival-time)
   :bus-schedule (->> (str/split bus-schedule #",")
                      (map #(if (= "x" %)
                              :out-of-service
                              (Integer/parseInt %))))})

(defn next-bus-time [base schedule]
  (cond
    (= :out-of-service schedule) Integer/MAX_VALUE
    (zero? (rem base schedule)) base
    :else (* schedule (inc (quot base schedule)))))

(defn solve-part-1 [input]
  (p* day 1
      (let [{:keys [arrival-time bus-schedule]} (parse input)
            bus-next-arrivals (map (fn [id] [id (next-bus-time arrival-time id)]) bus-schedule)
            [id next-time] (apply min-key second bus-next-arrivals)
            waiting-time (- next-time arrival-time)]
        (println :part1 arrival-time bus-schedule bus-next-arrivals [id next-time waiting-time])
        (* id waiting-time))))

(defn convert-requirements
  "Convert the requirements from:
  [[ai a] [bi b] ...] meaning n = ax-ai = by-bi = ...
  to [[ai' a] [bi' b] ...] meaning n = ax+ai' = by+bi'
  We assume a, b, c, etc are all prime"
  [reqs]
  (map (fn [[i p]] [(mod (- i) p) p]) reqs))

(defn solve-for-two
  "Find n = ax+ai = by+bi for a given a,ai,b,bi"
  [[ai a] [bi b]]
  (if (> a b) ; Faster to iterate with the larger multiple
    (->> (range ai Long/MAX_VALUE a) ; ai+a, ai+2a, ai+3a
         (filter #(zero? (rem (- % bi) b))) ; filter for n = by+bi by (n-bi)|b
         first ; get first
         )
    (solve-for-two [bi b] [ai a])))

(defn reduce-problem
  "We can reduce the problem of finding n = a*x+ai = b*y+bi = c*z+ci = ...
   to let n_ab = ax+ai = by+bi
      then n = lcm(a,b)*x+n_ab = c*z+ci = ...
  This function finds n_ab and lcm(a,b). Since a and b must be co-prime, lcm(a,b) = a*b"
  [[ai a] [bi b]]
  (println :reduce-problem [ai a] [bi b])
  (let [solution (solve-for-two [ai a] [bi b])
        lcm (* a b)]
    [solution lcm]))

(defn solve-part-2 [input]
  (p* day 2
      (let [{:keys [bus-schedule]} (parse input)
            requirements (->> (map-indexed vector bus-schedule)
                              (filter #(not= :out-of-service (second %))))
            reqs-converted (convert-requirements requirements)
            [solution _] (reduce reduce-problem reqs-converted)]
        solution)))

(comment
  (parse example-input)
  (solve-part-1 example-input)

  (solve-part-2 example-input)
  (solve-part-2 ["1" "17,x,13,19"]) ;=> 3417

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
