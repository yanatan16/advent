(ns advent.day18
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 18)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "1 + 2 * 3 + 4 * 5 + 6"))

(defn read-parenthetical [s]
  (loop [depth 0
         capture []
         [next-char & rest-s] s]
    (case next-char
      \( (recur (inc depth) (conj capture next-char) rest-s)
      \) (if (zero? (dec depth))
           [(apply str (rest capture)) (apply str rest-s)]
           (recur (dec depth) (conj capture next-char) rest-s))
      (recur depth (conj capture next-char) rest-s))))

(assert (= ["1 2 3" ""] (read-parenthetical "(1 2 3)")))
(assert (= ["1 2 3" " (4 5 6)"] (read-parenthetical "(1 2 3) (4 5 6)")))
(assert (= ["1 (2) 3" " (4 5 6)"] (read-parenthetical "(1 (2) 3) (4 5 6)")))

(declare lex)

(defn lex-token [s]
  (let [s (str/trim s)]
    (if-let [[_ number op rest] (re-find #"^(?:(\d+)|(\+|\*))(.*)$" s)]
      [(cond number [:number (Integer/parseInt number)]
             (= op "*") [:op *]
             (= op "+") [:op +])
       rest]
      (if (= \( (first s))
        (let [[paren rest] (read-parenthetical s)]
          [[:paren (lex paren)] rest])
        (throw (ex-info "couldnt read token" {:s s}))))))

(assert (= [[:number 5] " * 10"] (lex-token "5 * 10")))
(assert (= [[:op *] " 10"] (lex-token " * 10")))
(assert (= [[:number 10] ""] (lex-token " 10")))

(defn lex [s]
  (loop [tokens [] s s]
    (if (empty? s)
      tokens
      (let [[token rest] (lex-token s)]
        (recur (conj tokens token) rest)))))

(assert (= [[:number 5] [:op *] [:number 10]] (lex "5 * 10")))
(assert (= [[:paren [[:number 5] [:op *] [:number 10]]]] (lex "(5 * 10)")))

(defn parse [lines]
  (map lex lines))

(defn eval-pt1 [token]
  #_(println :eval-pt1 token)
  (cond
    (= :number (first token)) (second token)
    (= :op (first token)) (throw (ex-info "cant evaluate operation" {:token token}))
    (= :paren (first token)) (eval-pt1 (second token))

    (and (vector? (first token))
         (= 1 (count token)))
    (eval-pt1 (first token))

    (and (vector? (first token))
         (= 2 (count token)))
    (throw (ex-info "two tokens left" {:token token}))

    (and (vector? (first token))
         (<= 3 (count token)))
    (let [[t1 [op opf] t3 & tokens] token]
      (if (not= :op op)
        (throw (ex-info "second token isnt an operation" {:token token}))
        (eval-pt1 (concat [[:number (opf (eval-pt1 t1) (eval-pt1 t3))]] tokens))))

    ))

(assert (= 5 (eval-pt1 [:number 5])))
(assert (= 8 (eval-pt1 [[:number 5] [:op +] [:number 3]])))
(assert (= 16 (eval-pt1 [[:number 5] [:op +] [:number 3] [:op *] [:number 2]])))
(assert (= 8 (eval-pt1 [:paren [[:number 5] [:op +] [:number 3]]])))
(assert (= 8 (eval-pt1 [[:paren [[:number 5] [:op +] [:number 3]]]])))

(defn solve-part-1 [input]
  (p* day 1
      (->> (parse input)
           (map eval-pt1)
           (apply +))))

(defn eval-pt2 [token]
  (cond
    (= :number (first token)) (second token)
    (= :op (first token)) (throw (ex-info "cant evaluate operation" {:token token}))
    (= :paren (first token)) (eval-pt2 (second token))

    (and (vector? (first token))
         (= 1 (count token)))
    (eval-pt2 (first token))

    (and (vector? (first token))
         (= 2 (count token)))
    (throw (ex-info "two tokens left" {:token token}))

    (and (vector? (first token))
         (<= 5 (count token))
         (= * (second (second token)))
         (= + (second (nth token 3))))
    (let [[t1 multiply t3 add t5 & tokens] token]
      (eval-pt2 (concat [t1 multiply [:number (eval-pt2 [t3 add t5])]] tokens)))

    (and (vector? (first token))
         (<= 3 (count token))
         (= :op (first (second token))))
    (let [[t1 [_ opf] t3 & tokens] token]
      (eval-pt2 (concat [[:number (opf (eval-pt2 t1) (eval-pt2 t3))]] tokens)))

    :else
    (throw (ex-info "second token isnt an operation" {:token token}))))

(assert (= 5 (eval-pt2 [:number 5])))
(assert (= 8 (eval-pt2 [[:number 5] [:op +] [:number 3]])))
(assert (= 16 (eval-pt2 [[:number 5] [:op +] [:number 3] [:op *] [:number 2]])))
(assert (= 25 (eval-pt2 [[:number 5] [:op *] [:number 3] [:op +] [:number 2]])))
(assert (= 8 (eval-pt2 [:paren [[:number 5] [:op +] [:number 3]]])))
(assert (= 8 (eval-pt2 [[:paren [[:number 5] [:op +] [:number 3]]]])))

(defn solve-part-2 [input]
  (p* day 2
      (->> (parse input)
           (map eval-pt2)
           (apply +))))


(comment
  (parse example-input)

  (solve-part-1 example-input)

  (solve-part-2 example-input)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
