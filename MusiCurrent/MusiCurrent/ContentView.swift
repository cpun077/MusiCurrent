//
//  ContentView.swift
//  MusiCurrent
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
                Spacer().frame(height: geometry.size.height / 7)
                
                Form {
                    HStack {
                        TextField(text: $viewModel.link) {
                            Text("Link")
                        }
                        Button(action: {
//                            UIApplication.shared.open(DataBridge.getDocumentsDirectory(), options: [:], completionHandler: nil)
                        }) {
                            Text("Choose Folder")
                                .frame(width: geometry.size.width / 10, height: geometry.size.height / 20)
                                .foregroundColor(.white)
                                .background(Color.gray)
                        }
                        .buttonStyle(PlainButtonStyle())
                        .cornerRadius(8)
                    }
                    .frame(width: geometry.size.width * 0.8)
                    Text("Your link must be from a supported platform.")
                }
                .frame(maxWidth: .infinity)
                Spacer().frame(height: geometry.size.height / 3)
                Button(action: {
                    withAnimation(.easeOut(duration: 0.3)) {
                        currentView = .subview
                    }
                    
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                        let runner = Runner()
                        if let downloads = FileManager.default.urls(for: .downloadsDirectory, in: .userDomainMask).first {
                            let sfolder = downloads.appendingPathComponent("Sounds")
                            if !FileManager.default.fileExists(atPath: sfolder.path) {
                                do {
                                    try FileManager.default.createDirectory(at: sfolder, withIntermediateDirectories: true)
                                } catch {
                                    print("Could not create a folder to dump files, using Downloads folder")
                                    runner.runScript(url: viewModel.link, dir: downloads.path)
                                }
                            }
                            runner.runScript(url: viewModel.link, dir: sfolder.path)
                        } else {
                            print("Could not access Downloads folder")
                        }
                    }
                }) {
                    Text("Submit")
                        .frame(width: geometry.size.width / 4, height: geometry.size.height / 12)
                        .foregroundColor(.white)
                        .background(Color.blue)
                }
                .buttonStyle(PlainButtonStyle())
                .cornerRadius(12)
            }
        }
    }
    
    var subview: some View {
        Text("Processing URL")
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
