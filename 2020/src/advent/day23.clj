(ns advent.day23
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 23)
(def input' (delay "643719258"))

(def example-input "389125467")

(defn decr-char [c]
  (if (= c \1) \9 (char (dec (int c)))))

(defn find-insertion [cups current]
  (->> [(decr-char current)
        (decr-char (decr-char current))
        (decr-char (decr-char (decr-char current)))]
       (map #(str/index-of cups %))
       (filter identity)
       first
       inc))

(defn play-move [cups]
  (let [current (first cups)
        removed (subs cups 1 4)
        leftover (subs cups 4)
        insertion-index (find-insertion leftover current)]
    (str (subs leftover 0 insertion-index)
         removed
         (subs leftover insertion-index)
         current)))

(assert (= "289154673" (play-move "389125467")))

(defn play [cups moves]
  (reduce (fn [cups _] (play-move cups)) cups (range moves)))

(defn output [cups]
  (let [index-1 (str/index-of cups \1)]
    (str (subs cups (inc index-1))
         (subs cups 0 index-1))))

(assert (= "92658374" (output "583741926")))

(defn solve-part-1 [input]
  (p* day 1
      (output (play input 100))))

(defn solve-part-2 [input]
  (p* day 2
      ))


(comment
  (parse example-input)

  (solve-part-1 example-input)

  (play example-input 1)
  (play example-input 2)
  (play example-input 3)
  (play example-input 10)

  (solve-part-2 example-input)

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
