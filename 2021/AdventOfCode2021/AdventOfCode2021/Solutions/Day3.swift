//
//  Day3.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day3 : Solution {
    var exampleRawInput: String { """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""}
    
    typealias Binary = [Int]
    typealias Input = [Binary]
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines()
            .filter{ $0.count > 0 }
            .map { row in
                row.compactMap { Int(String($0)) }
            }
        
    }
    
    func binaryToInt(_ bits: Binary) -> Int {
            bits.reversed().enumerated().map { (index, digit) in
                //print("index \(index) digit \(digit)")
                return digit * twoToThePowerOf(index)
            }.sum()
    }
    
    func calcGamma(_ input: Input) -> Int {
        let gamma : Binary = input.transpose().map { column in
            if column.sum() > column.count / 2 {
                return 1
            } else {
                return 0
            }
        }
        return binaryToInt(gamma)
    }

    func calcEpsilon(_ input: Input, gamma: Int) -> Int {
        twoToThePowerOf(input.first!.count) - 1 - gamma
    }
    
    func problem1(_ input: Input) -> Int {
        let gamma = calcGamma(input)
        let epsilon = calcEpsilon(input, gamma: gamma)
        
        print("Gamma: \(gamma), Epsilon: \(epsilon)")
        return gamma * epsilon
    }
    
    func calcRating(_ input: Input, isMostCommon: Bool, position: Int) -> Int {
        let consideredValues = input.map { row in row[position] }
        let mostCommonValue = consideredValues.sum() * 2 >= input.count ? 1 : 0
        let keepValue = isMostCommon ? mostCommonValue : (1 - mostCommonValue)
        
        let filteredInput = input.filter { row in row[position] == keepValue }
        
        if filteredInput.count == 1 {
            return binaryToInt(filteredInput.first!)
        } else {
            return calcRating(filteredInput, isMostCommon: isMostCommon, position: position + 1)
        }
    }
    
    func calcRating(_ input: Input, isMostCommon: Bool) -> Int {
        calcRating(input, isMostCommon: isMostCommon, position: 0)
    }
    
    func problem2(_ input: Input) -> Int {
        let oxygen = calcRating(input, isMostCommon: true)
        let co2 = calcRating(input, isMostCommon: false)
        print("oxygen \(oxygen) co2 \(co2)")
        return oxygen * co2
    }
}
