//
//  App.swift
//  MusiCurrent
//
//  Created by Caden Pun on 3/1/24.
//

import SwiftUI
import AppKit

@main
struct MusiCurrentApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 700, minHeight: 500)
        }
    }
}


class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        if let window = NSApplication.shared.windows.first {
            window.center()
        }
    }
}
