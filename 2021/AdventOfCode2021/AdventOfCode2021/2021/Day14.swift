//
//  Day14.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/14/21.
//

import Foundation

// start: 7:08
// part 1: 7:24:16
// time: 0:16:16
// finish: 7:55:25
// time: 0:47:25
struct Day14 : Solution {
    var exampleRawInput: String { """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""}
    
    typealias InsertionRule = (from: String, to: String)
    struct Input {
        let template: String
        let insertionRules: [String:Character]
    }
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        let split = raw.split2lines()
        return Input(
            template: split[0],
            insertionRules: split[1].splitlines().reduce(into:[:]) { (map, line) in
                let pair = line.components(separatedBy: " -> ")
                map[pair[0]] = pair[1].first!
            }
        )
    }
    
    func iterate(_ input:Input, polymer: [Character]) -> [Character] {
        let insertedChars:[Character] = zip(polymer, polymer[1...]).flatMap { (c1, c2) -> [Character] in
            guard let insert = input.insertionRules[String([c1,c2])]
            else {
                return [c1]
            }
            return [c1, insert]
        }
        
        return insertedChars + [polymer.last!]
    }
    
    func answer(_ polymer: [Character]) -> Int {
        let frequencies = polymer.reduce(into:[:]) { (map, char) in
            map[char, default:0] += 1
        }.values.map { $0 }.sorted()
        
        return frequencies.last! - frequencies.first!
    }
    
    func problem1(_ input: Input) -> Int {
        let finalPolymer = (1...10).reduce(input.template.map{$0}) { (polymer, iter) in
            // print("\(iter): \(templateToFreqs(String(polymer)))")
            return iterate(input, polymer: polymer)
        }
        
        return answer(finalPolymer)
    }
    
    func smartAnswer(_ input: Input, _ pairFreqs: [String:Int]) -> Int {
        // Using freqs, we calculate the count of each character
        // then subtract 1 from first and last of input template
        // Since those never change and aren't reused
        let charFreqs:[Character:Int] = pairFreqs.reduce(into:[:]) { (freqs, kv) in
            freqs[kv.key.first!, default:0] += kv.value
            freqs[kv.key.last!, default:0] += kv.value
        }
        let freqs:[Int] = charFreqs.map { (char, count) in
            if char == input.template.first! ||
                char == input.template.last! {
                return (count + 1) / 2
            } else {
                return count / 2
            }
        }.sorted()
        return freqs.last! - freqs.first!
    }
    
    func smartIteration(_ input: Input, _ pairFreqs: [String:Int]) -> [String:Int] {
        pairFreqs.reduce(into: [:]) { (nextFreqs, kv) in
            let pair = kv.key
            let count = kv.value
            if let insert = input.insertionRules[pair] {
                nextFreqs[String([pair.first!, insert]), default: 0] += count
                nextFreqs[String([insert, pair.last!]), default: 0] += count
            } else {
                nextFreqs[pair, default: 0] += count
            }
        }
    }
    
    func templateToFreqs(_ template: String) -> [String:Int] {
        zip(template.map{$0}, template.map{$0}[1...])
           .reduce(into:[:]) { (freqs, pair) in
               freqs[String([pair.0, pair.1]), default:0] += 1
           }
    }
    
    func problem2(_ input: Input) -> Int {
        let startingFrequencies = templateToFreqs(input.template)
        let finalPolymer = (1...40).reduce(startingFrequencies) { (polymerFreqs, iter) in
            // print("\(iter): \(polymerFreqs)")
            return smartIteration(input, polymerFreqs)
        }
        
        // print("final: \(finalPolymer.values.sorted())")
        return smartAnswer(input, finalPolymer)
    }
}


