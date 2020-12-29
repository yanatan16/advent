(ns advent.day21
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 21)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"))

(defn parse-line [line]
  (if-let [[_ ingredients allergens] (re-find #"^([a-z ]+) \(contains ([a-z, ]+)\)$" line)]
    {:ingredients (str/split ingredients #" ")
     :allergens (str/split allergens #", ")}
    (throw (ex-info "couldnt parse line" {:line line}))))

(defn parse [input]
  (map parse-line input))

(defn solve-part-1 [input]
  (p* day 1
      (let [foods (parse input)
            all-ingredients (mapcat :ingredients foods)
            all-ingredients-freq (frequencies all-ingredients)
            all-ingredients-set (set all-ingredients)]
        (->> foods
             (map (fn [{:keys [allergens ingredients]}]
                    (->> allergens
                         (map (fn [allergen] {allergen (set ingredients)}))
                         (apply merge))))
             (apply merge-with set/intersection)
             vals
             (apply set/union)
             (set/difference all-ingredients-set)
             (map #(get all-ingredients-freq %))
             (apply +)))))

(defn basic-dangerous-ingredients [foods]
  (->> foods
       (map (fn [{:keys [allergens ingredients]}]
              (->> allergens
                   (map (fn [allergen] {allergen (set ingredients)}))
                   (apply merge))))
       (apply merge-with set/intersection)))

(defn safe-ingredients [foods]
  (let [all-ingredients (mapcat :ingredients foods)
        all-ingredients-set (set all-ingredients)]
    (->> foods
         basic-dangerous-ingredients
         vals
         (apply set/union)
         (set/difference all-ingredients-set))))

(defn determine-allergens [foods]
  (loop [ingredient->allergen {}
         allergen->ingredients (basic-dangerous-ingredients foods)]
    (cond
      (empty? allergen->ingredients) ingredient->allergen

      (some #(= 1 (count (second %))) allergen->ingredients)
      (let [[allergen single-ingredient-set] (some #(if (= 1 (count (second %))) %) allergen->ingredients)
            ingredient (first single-ingredient-set)]
        (recur (assoc ingredient->allergen ingredient allergen)
               (->> (dissoc allergen->ingredients allergen)
                    (map (fn [[allergen ingredient-set]] [allergen (disj ingredient-set ingredient)]))
                    (into {}))))

      :else
      (throw (ex-info "couldnt determine allergens" {:allergen->ingredients allergen->ingredients
                                                     :ingredient->allergen ingredient->allergen})))))

(defn solve-part-2 [input]
  (p* day 2
      (let [foods (parse input)
            ingredient->allergen (determine-allergens foods)]
        (->> ingredient->allergen
             (sort-by second)
             (map first)
             (str/join ",")))))


(comment
  (parse example-input)

  (solve-part-1 example-input)

  (basic-dangerous-ingredients (parse example-input))

  (solve-part-2 example-input)

  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
