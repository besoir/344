import scala.util.parsing.combinator._
 
abstract class Tree
case class E(m: Tree) extends Tree
case class And(l: Tree, r: Tree) extends Tree
case class Or(l: Tree, r: Tree) extends Tree
case class Not(r: Tree) extends Tree
case class Chr(n: Char) extends Tree
case class Bool(b: Boolean) extends Tree
//case class Parab(p: Char) extends Tree
//case class Parae(q: Char) extends Tree
 
object TreeBuilder extends Definitions {
  type Environment = String => String

  def eval(t: Tree, env: Environment): String = t match {
    //The E Case
    //The case e + the value of the statement is true => return just the string true
    case E(m) if(eval(m, env) == "true") => "true" 
    //The case e + the value of the statement is false => return just the string false
    case E(m) if(eval(m, env) == "false") => "false" 
    //The case e => value of the statement
    case E(m) => "(" + eval(m, env) + ")"

    //The And Cases
    //The case and + left side is true => the statement = value of the right side
    case And(l, r) if(eval(l,env) == "true") => eval(r, env)
    //The case and + left side is false => the statement is false
    case And(l, r) if(eval(l, env) == "false") => "false"
    //The case and + the left /= true || false && the right is true => the statement = the left side
    case And(l, r) if(eval(r, env) == "true") => eval(l, env)
    //The case and + left /= true || false && the right is false => the statement is false
    case And(l, r) if(eval(r, env) == "false") => "false"
    //The case and + left, right /= true || false => the statement = value on right and value on the left
    case And(l, r) => eval(l, env) + "&&" + eval(r, env)
    
    //The Or Cases
    //The case or + left side is true => the statement is true
    case Or(l, r) if(eval(l, env) == "true") => "true"
    //The case or + left side is false => the statement = value of the left side
    case Or(l, r) if(eval(l, env) == "false")=> eval(r, env)
    //The case or + left /= true || false && the right is true => the statement is true
    case Or(l, r) if(eval(r, env) == "true") => "true"
    //The case or + left /= true || false && the right is false => the statement = the left side
    case Or(l, r) if(eval(r, env) == "false") => eval(l, env)
    //The case or + left, right /= true || false => the statement = value on right and value on left
    case Or(l, r) => eval(l, env) + "||" + eval(r, env)

    //The Not Case
    //The case not + the statement is true => the statement is false
    case Not(r) if(eval(r, env) == "true") => "false"
    //The case not + the statement is false => the statement is true
    case Not(r) if(eval(r, env) == "false") => "true"
    //The case not + the statement is neither true || false => the statement is false
    case Not(r) => "!" + (eval(r, env))

    //The Character Case
    //The case is a character => the value is the character
    case Chr(n) => "" + n
    
    //The Boolean Case
    //The case is a boolean => the value is that boolean
    case Bool(b) => "" + b
  }

  def main(args: Array[String]){
    print("expression? ")
    var in : String = scala.io.StdIn.readLine()
    while(in != "quit") {
      val out:Tree = parseAll(e, in).get
      val env: Environment = {
        case "a" => "a"
      }
      println("result: " + eval(out, env))
      print("expression? ")
      in = scala.io.StdIn.readLine()
    }  
  }
}
 
class Definitions extends JavaTokenParsers {
  //E -> T '||' E | T
  //T -> F '&&' T | F
  //F -> '!' A | A
  //A -> '(' E ')' | C
  //C -> 'true' | 'false' | 'c'
  //c -> anyChar

  def e: Parser[Tree] = t ~ orn ~ e ^^ {case l ~ o ~ r => Or(l, r)} | t
  def t: Parser[Tree] = f ~ andn ~ t ^^ {case l ~ a ~ r => And(l, r)} | f
  def f: Parser[Tree] = notn ~ a ^^ {case n ~ r => Not(r)} | a
  def a: Parser[Tree] = parab ~ e ~ parae ^^ {case l ~ m ~ r => E(m)} | c
  def c: Parser[Tree] = bol | chr
  def chr: Parser[Chr] = "[A-Za-z]".r ^^ {str => Chr(str.charAt(0))}
  def bol: Parser[Bool] = "true".r ^^ {str => Bool(true)} | "false".r ^^ {str => Bool(false)}
  def parab[Tree] = "("
  def parae[Tree] = ")"
  def andn[Tree] = "&&"
  def notn[Tree] = "!" 
  def orn[Tree] = "||"
}