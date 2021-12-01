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
     :inner (rest (butlast (map #(rest (butlast %)) rows)))
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
       frequencies
       (filter (fn [[tile-num edge-count-times-2]] (= 4 edge-count-times-2)))
       (map first)))

(defn flip [pic]
  (map reverse pic))

(defn flip-vert [pic]
  (reverse pic))

(defn rotate-ccw
  "this one weird trick rotates rows by 90 degs ccw"
  [pic]
  (flip (apply map vector pic)))

(defn rotate-180 [pic]
  (flip (flip-vert pic)))

(defn rotate-cw [pic]
  (rotate-180 (rotate-ccw pic)))

(let [pic (:inner (first (parse example-input)))]
  (assert (not= pic (flip pic)))
  (assert (= pic (flip (flip pic))))
  (assert (= pic (flip-vert (flip (rotate-ccw (rotate-ccw pic))))))
  (assert (= pic (rotate-cw (rotate-ccw pic))))
  (assert (= (rotate-180 pic) (rotate-ccw (rotate-ccw pic)))))

(defn tile-map [tiles matches]
  (reduce (fn [tm [t1 t2 [[e1 e2]]]]
            (assoc-in tm [t1 :matches t2] [e1 e2]))
          (reduce #(assoc %1 (:tile-num %2) %2) {} tiles)
          matches))



(defn build-image [tmap top-left-num]
  (let [top-left (tmap top-left-num)
        side-length (int (Math/sqrt (count tiles)))]
    (loop [image [] left top-left]
      (if (= side-length (count image))
        image
        (let [row (build-row tmap left side-length)
              image' (assoc-in image (count image) row)
              left' (find-below tmap left)]
          (recur image' left'))))))

(def sea-monster
  (->> "                  #
#    ##    ##    ###
 #  #  #  #  #  #   "
       str/split-lines
       (map (fn [line] (map #(case % \# true nil))))))

(defn matches-sea-monster? [image]
  (->> (every? (fn [[monster-line img-line]]
                 (every? (fn [monster-pix img-pix]
                           (or (false? monster-pix)
                               (= \# img-pix)))
                         (map vector monster-line img-line)))
               (map vector sea-monster image))))

(defn count-sea-monsters [image]
  (count
   (for [i (range (- (count image) 3))
         :let [sub-image (take 3 (drop i image))]
         :when (matches-sea-monster? sub-image)]
     1)))

(defn count-hashes [image]
  (->> image
       (map (fn [line] (count (filter #(= \# %) line))))
       (apply +)))

(defn solve-part-2 [input]
  (p* day 2
      (let [tiles (parse input)
            matches (all-tile-edge-matches tiles)
            tmap (tile-map tiles matches)
            corners (corners matches)
            top-left-tile-num (first corners)
            image (build-image tmap top-left-tile-num)]
        (first
         (for [img [image (flip image) (flip-vert image) (rotate-180 image)
                    (rotate-ccw image) (flip (rotate-ccw image)) (flip-vert (rotate-ccw image)) (rotate-cw image)]
               :let [sea-monsters (count-sea-monsters img)]
               :when (< 0 sea-monsters)]
           (- (count-hashes img)
              (* sea-monsters 15)))))))


(comment
  (parse example-input)

  (matching-edges (first (parse example-input)) (second (parse example-input)))
  (frequencies (mapcat #(take 2 %) (all-tile-edge-matches (parse example-input))))

  (solve-part-1 example-input)

  (solve-part-2 example-input)

  (count (parse @input'))

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
