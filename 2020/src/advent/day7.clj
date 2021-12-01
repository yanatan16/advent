(ns advent.day7
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]
            [loom.graph :as graph]
            [loom.alg :as alg]))

(def day 7)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."))

(defn clean [s]
  (str/trim (str/replace s #"bags?" "")))

(defn parse-line [line]
  (let [[source contain] (str/split (str/replace line "." "") #" contain ")]
    (if (not= contain "no other bags")
      (->> (str/split contain #", ")
           (map (fn [n-bags-s]
                  (if-let [[_ n bag] (re-find #"^(\d+) (.* bags?)$" n-bags-s)]
                    [(clean source) (clean bag) (Integer/parseInt n)]
                    (throw (ex-info "Failed to parse n-bags-s" {:n-bags-s n-bags-s}))))))
      [])))

(assert (= '(["light red" "bright white" 1]
             ["light red" "muted yellow" 2])
           (parse-line "light red bags contain 1 bright white bag, 2 muted yellow bags.")))

(defn solve-part-1 [input]
  (p* day 1
      (let [edges (mapcat parse-line input)
            weightless-edges (map #(take 2 %) edges)
            weightless-reverse-edges (map reverse weightless-edges)
            g (apply graph/digraph weightless-reverse-edges)]
        (dec (count (alg/bf-traverse g "shiny gold"))))))

(assert (= 4 (solve-part-1 example-input)))

(defn count-bags [g node]
  (->> (graph/successors g node)
       (map #(let [bags (graph/weight g node %)]
               (+ bags (* bags (count-bags g %)))))
       (apply +)))

(defn solve-part-2 [input]
  (p* day 2
      (let [edges (mapcat parse-line input)
            g (apply graph/weighted-digraph edges)]
        (count-bags g "shiny gold"))))

(assert (= 32 (solve-part-2 example-input)))

(comment
  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
