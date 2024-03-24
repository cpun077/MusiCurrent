//
//  FilePicker.swift
//  MusiCurrent
//
//  Created by Caden Pun on 3/24/24.
//

import Foundation
import AppKit

class FilePicker: NSObject, NSOpenSavePanelDelegate {
    var parent: ContentView?
    
    func openPanel(completion: @escaping (URL?) -> Void) {
        let openPanel = NSOpenPanel()
        openPanel.delegate = self
        openPanel.canChooseDirectories = true
        openPanel.canChooseFiles = false
        openPanel.canCreateDirectories = true
        openPanel.allowsMultipleSelection = false
        openPanel.prompt = "Choose"
        openPanel.begin { (result) in
            if result.rawValue == NSApplication.ModalResponse.OK.rawValue {
                guard let url = openPanel.url else {
                    completion(nil)
                    return
                }
                completion(url)
            } else {
                completion(nil)
            }
        }
    }
}
