//
//  ContentView.swift
//  playlist-localizer
//
//  Created by Caden Pun on 3/1/24.
//

import SwiftUI

struct ContentView: View {
    @State var link = ""
    
    var body: some View {
        GeometryReader { geometry in
            NavigationView {
                VStack {
                    Spacer().frame(height: geometry.size.height*0.1)
                    Form {
                        Section {
                            TextField("Link", text: $link)
                        }
                        Section(footer: Text("Your link must be from a supported platform.")) {
                        }
                    }
                    Button(action: {
                        // Your button action
                    }) {
                        Text("Submit")
                            .frame(width: geometry.size.width / 2, height: geometry.size.height / 15)
                            .foregroundColor(.white)
                            .background(Color.blue)
                            .cornerRadius(10)
                    }
                    Spacer().frame(height: geometry.size.height*0.15)
                }
                .navigationTitle("Paste Playlist")
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
