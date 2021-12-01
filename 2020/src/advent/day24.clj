(ns advent.day24
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 24)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"))

(defn parse-line [chars]
  (case (first chars)
    nil []
    \w (concat [:west] (parse-line (rest chars)))
    \e (concat [:east] (parse-line (rest chars)))
    \n (case (second chars)
         nil (throw (ex-info "got n without follow" {:chars chars}))
         \w (concat [:northwest] (parse-line (drop 2 chars)))
         \e (concat [:northeast] (parse-line (drop 2 chars))))
    \s (case (second chars)
         nil (throw (ex-info "got s without follow" {:chars chars}))
         \w (concat [:southwest] (parse-line (drop 2 chars)))
         \e (concat [:southeast] (parse-line (drop 2 chars))))))

(defn reduce-directions [directions]
  (let [freqs (frequencies directions)
        x (+ (:east freqs 0)
             (:northeast freqs 0)
             (- (:west freqs 0))
             (- (:southwest freqs 0)))
        y (+ (:west freqs 0)
             (:northwest freqs 0)
             (- (:east freqs 0))
             (- (:southeast freqs 0)))
        z (+ (:southwest freqs 0)
             (:southeast freqs 0)
             (- (:northwest freqs 0))
             (- (:northeast freqs 0)))]
    [x y z]))

(defn black-tiles
  "Instead of walking the paths, we just add up the final coordinates using reduce-directions
  and take a frequency map of all flipped tiles, then finding the ones flipped an odd number of times."
  [directions]
  (->> (map reduce-directions directions)
       frequencies
       (filter #(odd? (second %)))
       (map first)))

(defn solve-part-1 [input]
  (p* day 1
      (->> (map parse-line input)
           black-tiles
           count)))

(defn adjacent-tiles [[x y z]]
  [[(inc x) (dec y) z]
   [(dec x) (inc y) z]
   [(inc x) y (dec z)]
   [(dec x) y (inc z)]
   [x (inc y) (dec z)]
   [x (dec y) (inc z)]])

(defn adj-black-tile-count [tile-set tile]
  (count (for [t (adjacent-tiles tile)
               :when (tile-set t)]
           t)))

(defn flip-tiles [black-tiles]
  (let [black-tile-set (set black-tiles)
        all-considered-tiles (set (concat black-tiles (mapcat adjacent-tiles black-tiles)))]
    (for [tile all-considered-tiles
          :let [adj-black (adj-black-tile-count black-tile-set tile)
                is-black? (contains? black-tile-set tile)]
          :when (or (and is-black? (<= 1 adj-black 2))
                    (and (not is-black?) (= 2 adj-black)))]
      tile)))

(defn solve-part-2 [input]
  (p* day 2
      (let [directions (map parse-line input)
            day-1-black-tiles (black-tiles directions)]
        (->> (range 100)
             (reduce (fn [tiles _] (flip-tiles tiles)) day-1-black-tiles)
             count))))


(comment
  (reduce-directions (parse-line (first example-input)))

  (solve-part-1 example-input)

  (solve-part-2 example-input)

  (count (flip-tiles (black-tiles (map parse-line example-input))))

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
