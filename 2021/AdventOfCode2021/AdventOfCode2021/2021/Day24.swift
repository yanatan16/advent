//
//  Day24.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

struct Day24 : Solution {
    var exampleRawInput: String { """
    """}
    
    
    typealias Variable = Character
    enum VariableOrLiteral {
        case variable(Variable)
        case literal(Int)
    }
    enum Instruction {
        case inp(Variable)
        case add(Variable, VariableOrLiteral)
        case mul(Variable, VariableOrLiteral)
        case div(Variable, VariableOrLiteral)
        case mod(Variable, VariableOrLiteral)
        case eql(Variable, VariableOrLiteral)
        
    }
    enum MONADError : Error {
        case noMoreInput
        case divideByZero(line: Int)
        case negativeModulo(line: Int)
    }
    typealias Input = MONAD
    typealias Output = Int
    
    func parseVarOrLiteral(_ s:String) -> VariableOrLiteral {
        if "xyzw".contains(s.first!) {
            return .variable(s.first!)
        } else {
            return .literal(Int(s)!)
        }
    }
    func parseInput(_ raw: String) -> Input {
        MONAD(program: raw.splitlines().map { line in
            let split = line.components(separatedBy: " ")
            switch split[0] {
            case "inp":
                return .inp(split[1].first!)
            case "add":
                return .add(split[1].first!, parseVarOrLiteral(split[2]))
            case "mul":
                return .mul(split[1].first!, parseVarOrLiteral(split[2]))
            case "div":
                return .div(split[1].first!, parseVarOrLiteral(split[2]))
            case "mod":
                return .mod(split[1].first!, parseVarOrLiteral(split[2]))
            case "eql":
                return .eql(split[1].first!, parseVarOrLiteral(split[2]))
            default:
                return .inp("0")
            }
        })
    }
    
    struct MONAD {
        let program: [Instruction]
        
        func run(input: [Int]) throws -> Int {
            var registers:[Character:Int] = [
                "x":0,
                "y":0,
                "z":0,
                "w":0
            ]
            var inputLeft = input
            
            let get:(VariableOrLiteral) -> Int = { vx in
                switch vx {
                case .variable(let vxv):
                    return registers[vxv]!
                case .literal(let i):
                    return i
                }
            }
            
            try program.enumerated().forEach { i, instruction in
                switch instruction {
                case .inp(let v):
                    guard let i = inputLeft.first
                    else { throw MONADError.noMoreInput }
                    inputLeft = inputLeft.dropFirst().map{$0}
                    registers[v] = i
                case .add(let v, let vx):
                    registers[v] = registers[v]! + get(vx)
                case .mul(let v, let vx):
                    registers[v] = registers[v]! * get(vx)
                case .div(let v, let vx):
                    let vxv = get(vx)
                    if vxv == 0 {
                        throw MONADError.divideByZero(line: i+1)
                    }
                    registers[v] = registers[v]! / get(vx)
                case .mod(let v, let vx):
                    let vxv = get(vx)
                    if registers[v]! < 0 || vxv <= 0 {
                        throw MONADError.negativeModulo(line: i+1)
                    }
                    registers[v] = registers[v]! % get(vx)
                    
                case .eql(let v, let vx):
                    if registers[v]! == get(vx) {
                        registers[v] = 1
                    } else {
                        registers[v] = 0
                    }
                }
            }
            
            return registers["z"]!
        }
    }
    
    
    func problem1(_ program: Input) -> Int {
        if program.program.count == 0 {
            return -1
        }
        
        print("result \(try! program.run(input: [4,1,2,9,9,9,9,4,8,7,9,9,5,9]))")
        
        // Solved by hand in accompanying Day24.md
        let serialNumber = 41299994879959
        let inputNumbers = serialNumber.description.map { Int(String($0))! }
        let validity = try! program.run(input: inputNumbers)
        print("result: \(validity)")
        
        return serialNumber
    }
    
    func problem2(_ program: Input) -> Int {
        // Solved by hand in accompanying Day24.md
        let serial = 11189561113216
        let inputNumbers = serial.description.map { Int(String($0))! }
        let validity = try! program.run(input: inputNumbers)
        print("result: \(validity)")
        return serial
    }
}
