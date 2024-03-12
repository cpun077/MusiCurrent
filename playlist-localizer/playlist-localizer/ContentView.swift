//
//  ContentView.swift
//  playlist-localizer
//
//  Created by Caden Pun on 3/1/24.
//

import SwiftUI

class FormViewModel: ObservableObject {
    @Published var link = ""
}

enum currentView {
    case root
    case subview
}

struct ContentView: View {
    @State var viewModel = FormViewModel()
    @State private var currentView : currentView = .root
    
    var body: some View {
        VStack {
            switch currentView {
            case .root:
                root
            case .subview:
                subview
            }
        }
        .toolbar {
            ToolbarItem(placement: .navigation) {
                Button(action: {
                    withAnimation(.easeOut(duration: 0.3)) {
                        currentView = .root
                    }
                }, label: {
                    Label("back", systemImage: "chevron.left")
                })
                .disabled(currentView == .root)
                .help("Go Back")
            }
        }
    }
    
    var root: some View {
        GeometryReader { geometry in
            VStack {
                Form {
                    Section(footer: Text("Your link must be from a supported platform.")) {
                        TextField("Link", text: $viewModel.link)
                    }
                }
                Button(action: {
                    withAnimation(.easeOut(duration: 0.3)) {
                        currentView = .subview
                    }
                    
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                        if let downloads = FileManager.default.urls(for: .downloadsDirectory, in: .userDomainMask).first {
                            let sfolder = downloads.appendingPathComponent("Sounds")
                            if !FileManager.default.fileExists(atPath: sfolder.path) {
                                do {
                                    try FileManager.default.createDirectory(at: sfolder, withIntermediateDirectories: true)
                                } catch {
                                    print("Could not create a folder to dump files, using Downloads folder")
                                    runScript(url: viewModel.link, dir: downloads.path)
                                }
                            }
                            runScript(url: viewModel.link, dir: sfolder.path)
                        } else {
                            print("Could not access Downloads folder")
                        }
                    }
                }) {
                    Text("Submit")
                        .frame(width: geometry.size.width / 2, height: geometry.size.height / 15)
                        .foregroundColor(.white)
                        .background(Color.blue)
                        .cornerRadius(15)
                }
            }
        }
    }
    
    var subview: some View {
        Text("Downloading Songs").frame(maxWidth: .infinity, maxHeight: .infinity)
            .onTapGesture {
                withAnimation(.easeOut(duration: 0.3)) {
                    currentView = .root
                }
            }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
