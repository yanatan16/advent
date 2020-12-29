(ns advent.day16
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 16)
(def input' (delay (get-double-lined-input day)))

(def example-input (str/split "class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12" #"\n\n"))

(def example-input-pt2 (str/split "class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9" #"\n\n"))

(defn parse-rule [line]
  (if-let [[_ name low1 up1 low2 up2] (re-find #"^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$" line)]
    {:name name
     :range1 [(Long/parseLong low1)
              (Long/parseLong up1)]
     :range2 [(Long/parseLong low2)
              (Long/parseLong up2)]}
    (throw (ex-info "Failed to parse rule" {:line line}))))

(defn parse [[rules your-ticket nearby-tickets]]
  {:rules (map parse-rule (str/split-lines rules))
   :your-ticket (map #(Long/parseLong %) (str/split (second (str/split-lines your-ticket)) #","))
   :nearby-tickets (->> (rest (str/split-lines nearby-tickets))
                        (map #(str/split % #","))
                        (map #(map (fn [v] (Long/parseLong v)) %)))})

(defn valid-for-rule? [{:keys [range1 range2]} value]
  (or (<= (first range1) value (second range1))
      (<= (first range2) value (second range2))))

(defn could-be-valid? [rules value]
  (some #(valid-for-rule? % value) rules))

(defn solve-part-1 [input]
  (p* day 1
      (let [{:keys [rules nearby-tickets]} (parse input)]
        (->> nearby-tickets
             (apply concat)
             (filter #(not (could-be-valid? rules %)))
             (apply +)))))

(defn valid-for-rule? [{[low1 up1] :range1 [low2 up2] :range2} value]
  (or (<= low1 value up1)
      (<= low2 value up2)))

(defn identify-fields-loop [field-names rules-left field-values]
  (let [new-field-names (->> (for [[field-index values] field-values
                                   :let [valid-rules (filter #(every? (partial valid-for-rule? %) values) rules-left)
                                         _ (println :valid-rules field-index values valid-rules)]
                                   :when (= 1 (count valid-rules))]
                               [(:name (first valid-rules)) field-index])
                             (into {})
                             (merge field-names))
        known-rules (set (keys new-field-names))
        known-fields (set (vals new-field-names))
        new-rules-left (filter #(not (contains? known-rules (:name %))) rules-left)
        new-field-values (filter #(not (contains? known-fields (first %))) field-values)]
    [new-field-names new-rules-left new-field-values]))

(defn identify-fields [rules tickets]
  (println :identify-fields rules tickets)
  (loop [n 0
         field-names {}
         rules-left rules
         field-values (map-indexed vector (apply map vector tickets))]
    (cond
      (< 100 n) (throw (ex-info "too many iterations" {:field-names field-names
                                                       :rules-left rules-left
                                                       :field-values field-values}))

      (empty? rules-left) field-names

      :else
      (let [[new-field-names new-rules-left new-field-values]
            (identify-fields-loop field-names rules-left field-values)]
        (recur (inc n) new-field-names new-rules-left new-field-values)))))

(defn solve-part-2 [input]
  (p* day 2
      (let [{:keys [rules your-ticket nearby-tickets]} (parse input)
            valid-nearby-tickets (filter (fn [ticket] (every? #(could-be-valid? rules %) ticket)) nearby-tickets)
            all-valid-tickets (conj valid-nearby-tickets your-ticket)
            fields (identify-fields rules all-valid-tickets)]
        (println :identified-fields fields)
        (->> fields
             (filter #(str/starts-with? (first %) "departure"))
             (map #(nth your-ticket (second %)))
             (apply *)))))


(comment
  (parse example-input)

  (solve-part-1 example-input)

  (identify-fields-loop
   {}
   [{:name "class" :range1 [1 3] :range2 [4 19]}]
   [[0 [11 3 15 5]]])

  (identify-fields-loop
   {}
   [{:name "class" :range1 [0 1] :range2 [4 19]}
    {:name "row" :range1 [0 5] :range2 [8 19]}]
   [[0 [11 3 15 5]] [1 [12 9 1 14]]])


  (valid-for-rule? {:name "class" :range1 [0 1] :range2 [4 19]} 3)

  (parse example-input-pt2)

  (let [{:keys [rules nearby-tickets]} (parse example-input-pt2)]
    (map (fn [ticket] (every? #(could-be-valid? rules %) ticket)) nearby-tickets))

  (solve-part-2 example-input-pt2)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
