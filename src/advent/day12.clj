(ns advent.day12
  (:require [advent.utils :refer :all]
            [clojure.set :as set]
            [clojure.string :as str]))

(def day 12)
(def input' (delay (get-lined-input day)))

(def example-input (str/split-lines "F10
N3
F7
R90
F11"))

(defn parse-line [line]
  (let [[_ action n] (re-find #"^([NSEWLRF])(\d+)$" line)]
    [(keyword action) (Integer/parseInt n)]))

(defn execute-action-pt1 [state [action n]]
  #_(println :execute-action state [action n])
  (case action
    :N (update-in state [:location :y] + n)
    :S (update-in state [:location :y] - n)
    :E (update-in state [:location :x] + n)
    :W (update-in state [:location :x] - n)
    :R (update-in state [:direction] + n)
    :L (update-in state [:direction] - n)
    :F (case (mod (:direction state) 360)
         0 (execute-action state [:E n])
         90 (execute-action state [:S n])
         180 (execute-action state [:W n])
         270 (execute-action state [:N n]))))

(defn solve-part-1 [input]
  (p* day 1
      (let [final-state (->> input
                             (map parse-line)
                             (reduce execute-action-pt1 {:location {:x 0 :y 0} :direction 0}))]
        (+ (Math/abs (get-in final-state [:location :x]))
           (Math/abs (get-in final-state [:location :y]))))))


(defn rotate-waypoint [state n]
  (let [{:keys [x y]} (:waypoint state)]
    (->> (case (mod n 360)
           0 {:x x :y y}
           90 {:x y :y (- x)}
           180 {:x (- x) :y (- y)}
           270 {:x (- y) :y x})
         (assoc state :waypoint))))

(defn move-toward-waypoint [state n]
  (-> state
      (update-in [:location :x] + (* n (get-in state [:waypoint :x])))
      (update-in [:location :y] + (* n (get-in state [:waypoint :y])))))

(defn execute-action-pt2 [state [action n]]
  #_(println :execute-action state [action n])
  (case action
    :N (update-in state [:waypoint :y] + n)
    :S (update-in state [:waypoint :y] - n)
    :E (update-in state [:waypoint :x] + n)
    :W (update-in state [:waypoint :x] - n)
    :R (rotate-waypoint state n)
    :L (rotate-waypoint state (- n))
    :F (move-toward-waypoint state n)))

(defn solve-part-2 [input]
  (p* day 2
      (let [initial-state {:location {:x 0 :y 0}
                           :waypoint {:x 10 :y 1}}
            final-state (->> input
                             (map parse-line)
                             (reduce execute-action-pt2 initial-state))]
        (+ (Math/abs (get-in final-state [:location :x]))
           (Math/abs (get-in final-state [:location :y]))))))

(comment
  (solve-part-1 example-input)

  (solve-part-2 example-input)


  (do
    (solve-part-1 @input')

    (solve-part-2 @input')
    )
  )
