//
//  IntCode.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/7/21.
//

import Foundation

class IntCode {
    var program : [Int]
    var input: [Int]
    var output: [Int] = []
    var instructionPointer : Int = 0
    var relativeBasePointer : Int = 0
    
    init(program: [Int], input: [Int]) {
        self.program = program
        self.input = input
    }
    
    convenience init(program: [Int]) {
        self.init(program: program, input: [])
    }
    
    enum RetCode {
        case halt
        case cont
    }
    
    enum IntCodeError : Error {
        case paramModeIsUnknown(Int)
        case opcodeIsUnknown(Int)
        case illegalModeOnSet(Int)
        case tooManyIterations
        case noMoreInput
    }
    
    func get(offset: Int, mode: Int) throws -> Int {
        let pointer = instructionPointer + offset
        let param = program[pointer]
        switch mode {
        case 0:
            return program[param]
        case 1:
            return param
        case 2:
            return program[param + relativeBasePointer]
        default:
            throw IntCodeError.paramModeIsUnknown(param)
        }
    }
    
    func set(offset: Int, mode: Int, value: Int) throws {
        let pointer = instructionPointer + offset
        let param = program[pointer]
        
        // print("set \(value) at [\(param)] (mode: \(mode))")
        
        switch mode {
        case 0:
            program[param] = value
        case 1:
            throw IntCodeError.illegalModeOnSet(mode)
        case 2:
            program[param + relativeBasePointer] = value
        default:
            throw IntCodeError.paramModeIsUnknown(mode)
        }
    }
    
    func step() throws -> RetCode {
        let instruction = program[instructionPointer]
        let opcode = instruction % 100
        let mode1 = (instruction % 1000 - instruction % 100) / 100
        let mode2 = (instruction % 10000 - instruction % 1000) / 1000
        let mode3 = (instruction % 100000 - instruction % 10000) / 10000
        
        // print("step: \(instruction) => \(opcode) \(mode1) \(mode2) \(mode3)")
        switch opcode {
        case 1:
            // add
            let v1 = try get(offset: 1, mode: mode1)
            let v2 = try get(offset: 2, mode: mode2)
            try set(offset: 3, mode: mode3, value: v1 + v2)
            instructionPointer += 4
            return .cont
        case 2:
            // multiply
            let v1 = try get(offset: 1, mode: mode1)
            let v2 = try get(offset: 2, mode: mode2)
            try set(offset: 3, mode: mode3, value: v1 * v2)
            instructionPointer += 4
            return .cont
        case 3:
            guard let i = input.first else {
                throw IntCodeError.noMoreInput
            }
            input = input.dropFirst().map{$0}
            try set(offset: 1, mode: mode1, value: i)
            instructionPointer += 2
            return .cont
            
        case 4:
            let v = try get(offset: 1, mode: mode1)
            output.append(v)
            instructionPointer += 2
            return .cont
            
        case 5:
            let v1 = try get(offset: 1, mode: mode1)
            if v1 != 0 {
                let v2 = try get(offset: 2, mode: mode2)
                instructionPointer = v2
            } else {
                instructionPointer += 3
            }
            return .cont
            
        case 6:
            let v1 = try get(offset: 1, mode: mode1)
            if v1 == 0 {
                let v2 = try get(offset: 2, mode: mode2)
                instructionPointer = v2
            } else {
                instructionPointer += 3
            }
            return .cont
            
        case 7:
            let v1 = try get(offset: 1, mode: mode1)
            let v2 = try get(offset: 2, mode: mode2)
            if v1 < v2 {
                try set(offset: 3, mode: mode3, value: 1)
            } else {
                try set(offset: 3, mode: mode3, value: 0)
            }
            instructionPointer += 4
            return .cont
            
        case 8:
            let v1 = try get(offset: 1, mode: mode1)
            let v2 = try get(offset: 2, mode: mode2)
            if v1 == v2 {
                try set(offset: 3, mode: mode3, value: 1)
            } else {
                try set(offset: 3, mode: mode3, value: 0)
            }
            instructionPointer += 4
            return .cont
            
        case 9:
            let v1 = try get(offset: 1, mode: mode1)
            relativeBasePointer += v1
            instructionPointer += 2
            return .cont
            
        case 99:
            return .halt
            
        default:
            throw IntCodeError.opcodeIsUnknown(opcode)
        }
    }
    
    func run() throws -> [Int] {
        for _ in 1...1000000 {
            switch try step() {
            case .halt:
                return output
            case .cont:
                continue
            }
        }
        throw IntCodeError.tooManyIterations
    }
    
    func runAscii() -> String {
        do {
            return try run().toAscii()
        } catch {
            print("IntCode error: \(error)")
            return ""
        }
    }
}
