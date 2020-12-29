(ns advent.utils
  (:require [clj-http.client :as http]
            [clojure.string :as str]
            [environ.core :refer [env]]))

(defn p* [day part result]
  (println (str "Day " day " Part " part " Result: " result))
  result)

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
