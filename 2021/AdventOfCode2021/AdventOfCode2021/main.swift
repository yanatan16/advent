//
//  main.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

let DEFAULT_DAY = "25"

var Runners:[String:Runner] = [
    "1":Day1().runner(),
    "2":Day2().runner(),
    "3":Day3().runner(),
    "4":Day4().runner(),
    "5":Day5().runner(),
    "6":Day6().runner(),
    "7":Day7().runner(),
    "8":Day8().runner(),
    "9":Day9().runner(),
    "10":Day10().runner(),
    "11":Day11().runner(),
    "12":Day12().runner(),
    "13":Day13().runner(),
    "14":Day14().runner(),
    "15":Day15().runner(),
    "16":Day16().runner(),
    "17":Day17().runner(),
    "18":Day18Rewrite().runner(),
    "19":Day19().runner(),
    "20":Day20().runner(),
    "21":Day21().runner(),
    "22":Day22().runner(),
    "23":Day23().runner(),
    "24":Day24().runner(),
    "25":Day25().runner(),
]

func defaultInputFile(day: String) -> String { "\(FileManager().homeDirectoryForCurrentUser.path)/dev/jon/advent/2021/inputs/input\(day).txt"
}

public func readInput(_ inputFile: String) -> String? {
    return try? String(contentsOfFile: inputFile,
                       encoding: String.Encoding.utf8)
}

func main(day: String, inputFile: String) {
    let rawInput = readInput(inputFile)
    
    if rawInput != nil {
        print("Read \(rawInput!.count) characters from \(inputFile)")
    } else {
        print("Didn't find Input File: \(inputFile)")
    }
    
    guard let runner = Runners[day] else {
        print("Didn't find solution for \(day)")
        exit(1)
    }
    
    runner.run(rawInput)
}

let args = CommandLine.arguments.dropFirst()
let day : String = args.first ?? DEFAULT_DAY
let inputFile : String = args.dropFirst().first ?? defaultInputFile(day: day)

main(day: day, inputFile: inputFile)
