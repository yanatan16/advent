(ns advent.day19-part2
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 19)
(def input' (delay (get-double-lined-input day)))

(def example-input (str/split "42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: \"a\"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: \"b\"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba" #"\n\n"))

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

(defn match-rule-8
  "Manually match for 8: 42 | 42 8
  We know only 8 and 11 contain infinite loops.
  So we create all possible matches and return them from here"
  [rules message]
  (if-let [msg (match-sub-rule rules [42] message)]
    (lazy-cat (list msg) (match-rule-8 rules msg))
    '()))

(assert (= '() (match-rule-8 {42 {:char \a}} "")))
(assert (= '(()) (match-rule-8 {42 {:char \a}} "a")))
(assert (= '((\a \a) (\a) ()) (match-rule-8 {42 {:char \a}} "aaa")))

(defn match-rule-11
  "Manually match for 11: 42 31 | 42 11 31
  We know only 8 and 11 contain infinite loops.
  So we create all possible matches and return them from here"
  [rules message]
  (if-let [match42 (match-sub-rule rules [42] message)]
    (let [match31 (match-sub-rule rules [31] match42)]
      (concat (if (some? match31) (list match31) '())
                (for [sub-match-42-11 (match-rule-11 rules match42)
                      :let [sub-match-42-11-31 (match-sub-rule rules [31] sub-match-42-11)]
                      :when (some? sub-match-42-11-31)]
                  sub-match-42-11-31)))
    '()))

(assert (= '() (match-rule-11 {42 {:char \a} 31 {:char \b}} "")))
(assert (= '() (match-rule-11 {42 {:char \a} 31 {:char \b}} "a")))
(assert (= '(()) (match-rule-11 {42 {:char \a} 31 {:char \b}} "ab")))
(assert (= '() (match-rule-11 {42 {:char \a} 31 {:char \b}} "aab")))
(assert (= '(()) (match-rule-11 {42 {:char \a} 31 {:char \b}} "aabb")))
(assert (= '((\a)) (match-rule-11 {42 {:char \a} 31 {:char \b}} "aabba")))

(defn match-rule-0? [rules message]
  (first
   (for [rule8-match (match-rule-8 rules message)
         rule11-match (match-rule-11 rules rule8-match)
         :when (and (some? rule11-match)
                    (empty? rule11-match))]
     true)))

(defn solve-part-2 [input]
  (p* day 1
      (let [{:keys [rules messages]} (parse input)]
        (->> messages
             (filter (partial match-rule-0? rules))
             count))))


(comment


  (solve-part-2 example-input)

  (do
    (solve-part-2 @input')

    )
  )
