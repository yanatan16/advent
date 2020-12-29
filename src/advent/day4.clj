(ns advent.day4
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 4)
(def input' (delay (get-raw-input day)))

(def required-fields
  #{"byr" "iyr" "eyr" "hgt" "hcl" "ecl" "pid"})

(defn parse [input]
  (for [passport-raw (str/split input #"\n\n")]
    (->> (str/split passport-raw #"[ \n]+")
         (map #(str/split % #":"))
         (into {}))))

(defn solve-part-1 [input]
  (p* day 1
      (->> (parse input)
           (map keys)
           (filter #(empty? (set/difference required-fields (set %))))
           count)))

(defn between? [n lower upper]
  (and (re-find #"^\d+$" n)
       (<= lower (Integer/parseInt n) upper)))

(defn byr-valid? [byr]
  (between? byr 1920 2002))

(defn iyr-valid? [iyr]
  (between? iyr 2010 2020))

(defn eyr-valid? [eyr]
  (between? eyr 2020 2030))

(defn hgt-valid? [hgt]
  (if-let [[_ height unit] (re-find #"^(\d+)(in|cm)$" hgt)]
    (case unit
      "cm" (between? height 150 193)
      "in" (between? height 59 76)
      nil)))

(defn hcl-valid? [hcl]
  (some? (re-find #"^#[0-9a-f]{6}$" hcl)))

(defn ecl-valid? [ecl]
  (contains? #{"amb" "blu" "brn" "gry" "grn" "hzl" "oth"} ecl))

(defn pid-valid? [pid]
  (some? (re-find #"^[0-9]{9}$" pid)))

(defn solve-part-2 [input]
  (p* day 2
      (->> (parse input)
           (filter #(empty? (set/difference required-fields (set (keys %)))))
           (filter #(byr-valid? (get % "byr")))
           (filter #(iyr-valid? (get % "iyr")))
           (filter #(eyr-valid? (get % "eyr")))
           (filter #(hgt-valid? (get % "hgt")))
           (filter #(hcl-valid? (get % "hcl")))
           (filter #(ecl-valid? (get % "ecl")))
           (filter #(pid-valid? (get % "pid")))
           count)))

(comment
  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
