(ns advent.day14
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 14)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"))

(defn parse-mask-value [mask]
  (map #(case % \X nil \1 1 \0 0) mask))

(defn parse-line [line]
  (if-let [[_ mem addr value mask mask-value] (re-find #"^(?:(mem)\[(\d+)\] = (\d+)|(mask) = ([X01]{36}))$" line)]
    (if mem
      {:instruction :mem
       :addr (Integer/parseInt addr)
       :value (Long/parseLong value)}
      {:instruction :mask
       :mask (parse-mask-value mask-value)})
    (throw (ex-info "Failed to parse line" {:line line}))))

(defn parse [input]
  (map parse-line input))

(defn value->bits [value]
  (->> (range 36)
       reverse
       (reduce (fn [[bits v] power]
                 (let [px (Math/pow 2 power)]
                   [(conj bits (int (quot v px)))
                    (rem v px)]))
               [[] value])
       first))

(defn bits->value [bits]
  (->> (reverse bits)
       (map-indexed #(* (Math/pow 2 %1) %2))
       (apply +)
       long))

(assert (= '(0 0 0 0
               0 0 0 0 0 0 0 0
               0 0 0 0 0 0 0 0
               0 0 0 0 0 0 0 0
               0 1 1 0 0 1 0 1)
           (value->bits 101)))

(assert (= (bits->value '(0 1 1 0 0 1 0 1))
           101))

(defn mask-bits [bits mask]
  (map (fn [bit mask-bit]
         (if (nil? mask-bit) bit mask-bit))
       bits mask))

(assert (= '(0 1 0 0 1 0 0 1)
           (mask-bits
            '(0 0 0 0 1 0 1 1)
            '(nil 1 nil nil nil nil 0 nil))))

(def initial-state
  {:mask (repeat 36 nil)
   :memory {}})

(defn pt1-run-instruction [state {:keys [instruction addr value mask]}]
  (case instruction
    :mask (assoc state :mask mask)
    :mem (assoc-in state [:memory addr] (-> value
                                            value->bits
                                            (mask-bits (:mask state))
                                            bits->value))))

(defn sum-all-memory [{:keys [memory]}]
  (->> (vals memory)
       (apply +)))

(defn solve-part-1 [input]
  (p* day 1
      (->> input
           parse
           (reduce pt1-run-instruction initial-state)
           sum-all-memory)))

(defn all-floating-masked-addrs [addr mask]
  (loop [out [[]]
         [addr-high & addr-rest] addr
         [mask-high & mask-rest] mask]
    (if (nil? addr-high)
      out
      (cond
        (nil? mask-high)
        (recur (concat (map #(conj % 0) out)
                       (map #(conj % 1) out))
               addr-rest
               mask-rest)

        (zero? mask-high)
        (recur (map #(conj % addr-high) out)
               addr-rest
               mask-rest)

        :else
        (recur (map #(conj % 1) out)
               addr-rest
               mask-rest)))))

(assert (= (sort '([0 0 1 1 1 0 1 0]
                   [0 0 0 1 1 0 1 1]
                   [0 0 0 1 1 0 1 0]
                   [0 0 1 1 1 0 1 1]))
           (sort (all-floating-masked-addrs
                  '(0 0 1 0 1 0 1 0)
                  '(0 0 nil 1 0 0 1 nil)))))

(defn pt2-run-instruction [state {:keys [instruction addr value mask]}]
  (case instruction
    :mask (assoc state :mask mask)
    :mem (->> (all-floating-masked-addrs (value->bits addr) (:mask state))
              (reduce #(assoc-in %1 [:memory %2] value) state))))

(def example-input-pt2 (str/split-lines "mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"))

(defn solve-part-2 [input]
  (p* day 2
      (->> input
           parse
           (reduce pt2-run-instruction initial-state)
           sum-all-memory)))

(comment
  (parse example-input)
  (solve-part-1 example-input)

  (solve-part-2 example-input-pt2)

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
