;Create a method that evaluates and statements
(defn evalAnd [exp]
  ;;remove true because 'and' can be disregarded
  ;;(let [andRemainder (remove true? exp)]
    ;;create a 'switch statement'
    (cond
      ;;if it contains any false it is automatically false
      (some false? exp) false
      
      ;;if there is only an and statement when we remove the false return true
      (= (count (remove true? exp)) 1) true
      
      ;;if there is only a variable and a statement return the variable
      ;;remove the trues and then check if the statement has less than two parts, return the first
      (= (count (remove true? exp)) 2) (nth (remove true? exp) 1)
      
      ;;if the first two vars are the same return the first
      (= (nth exp 1) (nth exp 2)) (nth exp 1)

      ;;if there is more than one variable return the remainder
      ;;remove the trues and then check if the statement has two or more parts, return the expression minus the trues
      (> (count (remove true? exp)) 2) (distinct (remove true? exp))
    )
  ;;)
)

;;Create a method that evaluates or statements
(defn evalOr [exp]
  ;;remove false becuase 'or' can be disregarded
  ;;(let [orRemainder (flatten(distinct(rest exp)))]
    ;;create a 'switch statement'
    (cond
      ;;if it contains any true it is automatically true
      (some true? exp) true

      ;;if we remove the falses and there is only an or statement the statement is false
      (= (count (remove false? exp)) 1) false

      ;;if we remove the falses and there is an or and a var then return the var
      (= (count (remove false? exp)) 2) (nth (remove false? exp) 1)

      ;;if both of the statements are the same var return the first
      (= (nth exp 1) (nth exp 2)) (nth exp 1)
      ;;if there is more than two variables in the remainder
      ;;remove the falses and then check if the statement has two or more parts, return the expression minus the false
      (> (count (remove false? exp)) 2) (distinct (remove false? exp))
    )
  ;;)
)

;;Create a that evaluates not statements
(defn evalNot [exp]
  ;;create a 'switch statement'
  (cond
    ;;if we were given true it is false
    (some true? exp) false
    ;;if we were given false it is true
    (some false? exp) true
    ;;if neither we return the full statement
    :else exp
  )
)

(defn bolt [exp]
  ;;This makes the expression go to the very base case and work out 
  ;;like if we had an and that contained an or we would eval the or then the and
  (let [exp (map (fn [i] 
         (if (seq? i)
           (bolt i) i
          )
        ) 
      exp)]
  exp
  ;;create a 'switch statement'
  (cond
    ;;if it is 'and' pass it to evalAnd
    (= (compare (nth exp 0) (symbol 'and)) 0) (evalAnd (remove (nth exp 0) exp))
    ;;if it is 'or' pass it to evalOr
    (= (compare (nth exp 0) (symbol 'or)) 0) (evalOr (remove (nth exp 0) exp))
    ;;if it is 'not' pass it to evalNot
    (= (compare (nth exp 0) (symbol 'not)) 0) (evalNot (remove (nth exp 0) exp))
    ;;returns true if needed
    :else true
    )
  )
)
;;Subs the variable definition that it was given
;;This was given on the website
;;It binds the defined variables in the expression to their true||false value
(defn deep-substitute [m l]
  (map (fn [i] 
         (if (seq? i)
           (deep-substitute m i)
           (m i i)
          )
        ) 
  l)
)

;;create the syntax for how we execute an evalexp
;;given on the website
;;pretty much means that we have to say:
;;(evalexp ;{varOne true||false varTwo true||false ... varN true||false} followed by and exp)
;;and it also throws us into our main loop "bolt"
(defn evalexp [exp bindings] (bolt (deep-substitute bindings exp)))