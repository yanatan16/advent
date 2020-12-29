(ns advent.day20
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]
            [advent.day20-example-input :refer [example-input]]))

(def day 20)
(def input' (delay (get-double-lined-input day)))

(defn parse-tile [tile]
  (let [[tile-line & rows] (str/split-lines tile)
        [_ tile-num] (re-find #"^Tile (\d+):$" tile-line)
        columns (apply map vector rows)]
    {:tile-num (Integer/parseInt tile-num)
     :edges [(first rows)
             (apply str (last columns))
             (apply str (reverse (last rows)))
             (apply str (reverse (first columns)))]}))

(defn parse [tiles]
  (map parse-tile tiles))

(defn matching-edges [tile1 tile2]
  (for [[i1 e1] (map-indexed vector (:edges tile1))
        [i2 e2] (map-indexed vector (:edges tile2))
        :when (or (= e1 e2) (= e1 (apply str (reverse e2))))]
    [i1 i2]))

(defn all-tile-edge-matches [tiles]
  (for [tile1 tiles
        tile2 tiles
        :when (not= tile1 tile2)
        :let [edges (matching-edges tile1 tile2)]
        :when (not-empty edges)]
    [(:tile-num tile1) (:tile-num tile2) edges]))

(defn solve-part-1 [input]
  (p* day 1
      (->> (parse input)
           all-tile-edge-matches
           (mapcat #(take 2 %))
           frequencies
           ;; All corners only have two edges, so we just find those tile nums
           (filter (fn [[tile-num edge-count-times-2]] (= 4 edge-count-times-2)))
           (map first)
           (apply *))))

(defn corners [matches]
  (->> matches
       (mapcat #(take 2 %))
       (filter (fn [[tile-num edge-count-times-2]] (= 4 edge-count-times-2)))
       (map first)))

(defn solve-part-2 [input]
  (p* day 2
      (let [tiles (parse input)
            matches (all-tile-edge-matches tiles)
            corners (corners matches)]
        ;;TODO
        )))


(comment
  (parse example-input)

  (matching-edges (first (parse example-input)) (second (parse example-input)))
  (frequencies (mapcat #(take 2 %) (all-tile-edge-matches (parse example-input))))

  (solve-part-1 example-input)

  (solve-part-2 example-input)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
