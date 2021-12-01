(ns advent.day19
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 19)
(def input' (delay (get-double-lined-input day)))

(def example-input (str/split "0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: \"a\"
5: \"b\"

ababbb
bababa
abbbab
aaabbb
aaaabbb" #"\n\n"))

(defn parse-rule [line]
  (if-let [[_ rule-num char] (re-find #"^(\d+): \"([a-z])\"$" line)]
    [(Integer/parseInt rule-num) {:char (first char)}]
    (if-let [[_ rule-num sub-rules] (re-find #"^(\d+): ([\d \|]+)$" line)]
      [(Integer/parseInt rule-num) {:sub-rules (->> (str/split sub-rules #" \| ")
                                                    (map #(map (fn [r] (Integer/parseInt r)) (str/split % #" "))))}]
      (throw (ex-info "couldnt parse" {:line line})))))

(defn parse [[rules messages]]
  {:rules (into {} (map parse-rule (str/split-lines rules)))
   :messages (str/split-lines messages)})

(declare match)
(defn match-sub-rule [rules sub-rule message]
  (loop [[next-rule & rest-rules] sub-rule
         msg message]
    (if (nil? next-rule)
      msg
      (if-let [rest-msg (match rules (get rules next-rule) msg)]
        (recur rest-rules rest-msg)
        nil))))

(defn match [rules {:keys [char sub-rules] :as rule} message]
  (cond
    char (if (= char (first message)) (rest message))
    sub-rules (some #(match-sub-rule rules % message) sub-rules)
    :else (throw (ex-info "rule isnt understood" {:rule rule}))))

(defn match-rule-0? [rules message]
  (let [m (match rules (get rules 0) message)]
    (and (some? m)
         (empty? m))))

(defn solve-part-1 [input]
  (p* day 1
      (let [{:keys [rules messages]} (parse input)]
        (->> messages
             (filter (partial match-rule-0? rules))
             count))))


(comment
  (parse example-input)
  ;; => {:rules {0 {:sub-rules ((4 1 5))}, 1 {:sub-rules ((2 3) (3 2))}, 2 {:sub-rules ((4 4) (5 5))}, 3 {:sub-rules ((4 5) (5 4))}, 4 {:char \a}, 5 {:char \b}}, :messages ["ababbb" "bababa" "abbbab" "aaabbb" "aaaabbb"]}

  (def test-rules {0 {:sub-rules ((4 1 5))}, 1 {:sub-rules ((2 3) (3 2))}, 2 {:sub-rules ((4 4) (5 5))}, 3 {:sub-rules ((4 5) (5 4))}, 4 {:char \a}, 5 {:char \b}})
  (match-rule-0? {0 {:char \a}} "a")
  (match-rule-0? {0 {:char \a}} "b")
  (match-rule-0? {0 {:sub-rules '((1))} 1 {:char \a}} "a")
  (match-rule-0? {0 {:sub-rules '((1))} 1 {:char \a}} "b")
  (match-rule-0? {0 {:sub-rules '((1))} 1 {:char \a}} "ab")


  (solve-part-1 example-input)

  (do
    (solve-part-1 @input')

    )
  )
