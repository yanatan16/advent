//
//  Day7.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day7 : Solution {
    var exampleRawInput: String { """
16,1,2,0,4,2,7,1,2,14
"""}
    
    typealias Input = [Int]
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().first!.components(separatedBy: ",").compactMap { Int($0) }
    }
    
    func fuelCost(_ input: Input, position: Int) -> Int {
        input.map { abs(position - $0) }.sum()
    }
    
    func problem1(_ input: Input) -> Int {
        // This is a least squares problem with 0 slope
        // Minimize sum((x - pos)^2)
        let mean = Double(input.sum()) / Double(input.count)
        let stdev = sqrt(input.map({ pow(Double($0) - mean,2.0) }).sum() / Double(input.count))
        print("mean \(mean)")
        print("variance \(stdev)")
        
        var costs = (Int(floor(mean-stdev))...Int(ceil(mean+stdev))).map { fuel in
            (fuel, fuelCost(input, position: fuel))
        }
        
        //print("costs \(costs)")
        
        return costs.min(by: { (p1, p2) in p1.1 <= p2.1 })!.1
    }
    
    func increasingFuelCost(_ input: Input, position: Int, chart: [Int]) -> Int {
        input.map { chart[abs(position - $0)] }.sum()
    }
    
    func problem2(_ input: Input) -> Int {
        var fuelCostChart : [Int] = [0]
        for i in 1...2000 {
            fuelCostChart.append(fuelCostChart.last! + i)
        }
        
        var costs = (input.min()!...input.max()!).map { fuel in
            (fuel, increasingFuelCost(input, position: fuel, chart: fuelCostChart))
        }
        return costs.min(by: { (p1, p2) in p1.1 <= p2.1 })!.1
    }
}
