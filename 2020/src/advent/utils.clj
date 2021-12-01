(ns advent.utils
  (:require [clj-http.client :as http]
            [clojure.string :as str]
            [environ.core :refer [env]]))

(defmacro p* [day part & forms]
  `(let [start# (System/currentTimeMillis)
         result# (do ~@forms)
         duration# (/ (- (System/currentTimeMillis) start#) 1000000.0)]
     (println (format "Day %d Part %d Time %.2fms Result: %s" ~day ~part duration# result#))
     result#))

(defn get-raw-input [day]
  (some->
   (format "https://adventofcode.com/2020/day/%s/input" day)
   (http/get {:headers {:Cookie (str "session=" (:advent-of-code-cookie env) ";")}})
   :body))

(defn get-lined-input [day]
  (-> (get-raw-input day)
      (str/split #"\n")))

(defn get-double-lined-input [day]
  (-> (get-raw-input day)
      (str/split #"\n\n")))

(defn get-input-ints [day]
  (->> (get-lined-input day)
       (map #(Integer/parseInt %))))

(defn get-input-longs [day]
  (->> (get-lined-input day)
       (map #(Long/parseLong %))))

(defn drop*
  ([n seq] (drop* n seq 0 (quot n 10)))
  ([total seq dropped part]
   (println (System/currentTimeMillis) :drop* (str dropped " / " total) (first seq))
   (let [to-drop (min (- total dropped) part)]
     (if (zero? to-drop)
       seq
       (drop* total (drop to-drop seq) (+ dropped to-drop) part)))))

(defn iterate-until* [f state until]
  (->> (iterate f state)
       (drop* (dec until))
       first))
