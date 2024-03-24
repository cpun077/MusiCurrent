//
//  Runner.swift
//  MusiCurrent
//
//  Created by Caden Pun on 3/5/24.
//

import Foundation
import PythonKit

class Runner {
    func runScript(url: String, dir: String) {
        let sys = Python.import("sys")
        let filename = "converter"
        let path = URL(fileURLWithPath: #file).deletingLastPathComponent().path
        
        if FileManager.default.fileExists(atPath: "\(path)/\(filename).py") {
            sys.path.insert(0, path)
            do {
                let file = try Python.attemptImport(filename)
                file.processlink(url, dir)
            } catch {
                print("Import Error: ", error)
            }
        }
    }
}
