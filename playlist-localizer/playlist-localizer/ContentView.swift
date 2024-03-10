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

struct ContentView: View {
    @State var viewModel = FormViewModel()
    
    var body: some View {
        GeometryReader { geometry in
            NavigationView {
                VStack {
                    Form {
                        Section(footer: Text("Your link must be from a supported platform.")) {
                            TextField("Link", text: $viewModel.link)
                        }
                    }
                    Button(action: {
                        // downloadsurl = "/Users/cadenpun/Downloads"
                        if let downloads = FileManager.default.urls(for: .downloadsDirectory, in: .userDomainMask).first {
                            let sfolder = downloads.appendingPathComponent("Sounds")
                            if !FileManager.default.fileExists(atPath: sfolder.path) {
                                do {
                                    try FileManager.default.createDirectory(at: sfolder, withIntermediateDirectories: true)
                                } catch {
                                    print("Could not create a folder to dump files, using Downloads folder")
                                    runScript(pl: viewModel.link, dir: downloads.path)
                                }
                            }
                            runScript(pl: viewModel.link, dir: sfolder.path)
                        } else {
                            print("Could not access Downloads folder")
                        }
                    }) {
                        Text("Submit")
                            .frame(width: geometry.size.width / 2, height: geometry.size.height / 15)
                            .foregroundColor(.white)
                            .background(Color.blue)
                            .cornerRadius(15)
                    }
                    .padding()
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .navigationTitle("Paste Playlist")
                .padding()
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
