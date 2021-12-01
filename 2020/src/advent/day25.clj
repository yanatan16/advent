(ns advent.day25
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 25)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "5764801\n17807724"))

(defn parse [input]
  (map #(Long/parseLong %) input))

(def MAGIC 20201227)

(defn lazy-transform
  "Transform a subject number in a lazy list. Take loop-size to get key values"
  ([subject] (lazy-transform subject 1))
  ([subject value]
   (let [value' (rem (* value subject) MAGIC)]
     (lazy-cat (list value') (lazy-transform subject value')))))

(defn onetime-transform [subject loop-size]
  (nth (lazy-transform subject) (dec loop-size)))

(def key-generating-transforms
  ;; The lazy nature effectively makes this pre-generated
  ;; we only take for safety (infinity is scary!)
  (take 1000000 (lazy-transform 7)))

(defn determine-loop-size [key]
  (->> (map-indexed vector key-generating-transforms)
       (filter #(= key (second %)))
       first
       first
       (#(if (nil? %) (throw (ex-info "key not found" {:key key})) %))
       inc))

(defn solve-part-1 [input]
  (p* day 1
      (let [[key1 key2] (parse input)
            loop1 (determine-loop-size key1)]
        (onetime-transform key2 loop1))))

(defn solve-part-2 [input]
  (p* day 2
      ))


(comment
  (parse example-input)

  (determine-loop-size (first (parse example-input)))
  (onetime-transform (second (parse example-input)) 8)

  (solve-part-1 example-input)

  (solve-part-2 example-input)

  (filter #(= 14788856 %) key-generating-transforms)

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
