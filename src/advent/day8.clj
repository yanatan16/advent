(ns advent.day8
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 8)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"))

(defn parse-line [line]
  (let [[_ instruction sign n] (re-find #"^(nop|acc|jmp) (\+|-)(\d+)$" line)]
    [(keyword instruction) (* (if (= "-" sign) -1 1)
                              (Integer/parseInt n))]))

(defn parse [input]
  (->> input
       (map parse-line)
       (filter identity)
       vec))

(defn run-instruction [[instruction n] accumulator line]
  #_(println :run-instruction instruction n {:accumulator accumulator :line line})
  (case instruction
    :nop [accumulator (inc line)]
    :acc [(+ accumulator n) (inc line)]
    :jmp [accumulator (+ line n)]))

(defn run-program [program]
  (loop [accumulator 0 line 0
         all-run-lines #{}]
    (cond
      (<= (count program) line)
      {:state :completed
       :accumulator accumulator}

      (contains? all-run-lines line)
      {:state :infinite-loop
       :accumulator accumulator
       :all-run-lines all-run-lines}

      :else
      (let [[accumulator' line'] (run-instruction (nth program line) accumulator line)]
        (recur accumulator' line' (conj all-run-lines line))))))

(defn edit-program [program line]
  (update program line #(let [[instruction n] %]
                          (if (= instruction :nop)
                            [:jmp n]
                            [:nop n]))))

(defn solve-part-1 [input]
  (p* day 1
      (-> (parse input)
          run-program
          :accumulator)))

(defn solve-part-2 [input]
  (p* day 2
      (let [program (parse input)
            all-run-lines (:all-run-lines (run-program program))
            changeable-lines (->> all-run-lines
                                 (filter #(let [[instruction n] (nth program %)]
                                            (and (#{:jmp :nop} instruction)
                                                 (not= [:nop 0] [instruction n])
                                                 (not= [:jmp 1] [instruction n]))))
                                 sort)]
        (first
         (for [change-line changeable-lines
               :let [program' (edit-program program change-line)
                     {:keys [state accumulator]} (run-program program')]
               :when (= :completed state)]
           accumulator)))))

(comment
  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
