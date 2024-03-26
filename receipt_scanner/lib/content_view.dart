import 'package:flutter/material.dart';
import 'package:receipt_scanner/process_image_page.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart' as firebase_storage;

class ContentView extends StatefulWidget {
  @override
  _ContentViewState createState() => _ContentViewState();
}

class _ContentViewState extends State<ContentView> {
  XFile? _capturedImage;
  bool _processing = false;
  void resetCapturedImage() {
    setState(() {
      _capturedImage = null;
    });
  }

  void _loadImage() async {
    final picker = ImagePicker();
    final pickedImage = await picker.pickImage(source: ImageSource.camera);
    if (pickedImage != null) {
      setState(() {
        _capturedImage = pickedImage;
      });
    }
  }

  void _processImage() async {
    setState(() {
      _processing = true;
    });

    if (_capturedImage != null) {
      final bytes = await _capturedImage!.readAsBytes();
      final fileName =
          DateTime.now().millisecondsSinceEpoch.toString() + '.jpg';
      final folderName = fileName.split('.').first;

      final ref = firebase_storage.FirebaseStorage.instance
          .ref('$folderName/$fileName');
      final uploadTask = ref.putData(bytes);

      await uploadTask;

      final imageUrl = await ref.getDownloadURL();
      print("Image URL: $imageUrl");

      final url =
          'http://192.168.2.17:5001/process_image?folderName=$folderName';
      final response = await http.post(
        Uri.parse(url),
        body: bytes,
        headers: {'Content-Type': 'application/octet-stream'},
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        final double totalAmount = responseData['total_amount'] ?? 0.0;
        final String date = responseData['date'] ?? '';
        final String category = responseData['category'] ?? '';

        print("Image processed successfully");
        setState(() {
          _processing = false;
        });
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ProcessedImagePage(
              imageUrl: imageUrl,
              totalAmount: totalAmount,
              date: date,
              category: category,
              resetCapturedImage: resetCapturedImage,
            ),
          ),
        );
      } else {
        print('Failed to process image: ${response.statusCode}');
        setState(() {
          _processing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: _capturedImage == null
            ? Container(
                height: MediaQuery.of(context).size.height,
                decoration:
                    BoxDecoration(color: Color.fromARGB(255, 217, 222, 224)),
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SizedBox(height: 350),
                      Align(
                        alignment: Alignment.centerLeft,
                        child: Padding(
                          padding: EdgeInsets.only(left: 20),
                          child: Text(
                            'scan·it',
                            style: TextStyle(
                                fontFamily: 'Porlane',
                                fontSize: 50,
                                fontWeight: FontWeight.w500,
                                letterSpacing: 2.0,
                                color: Colors.black),
                          ),
                        ),
                      ),
                      SizedBox(height: 10),
                      Align(
                        alignment: Alignment.centerLeft,
                        child: Padding(
                          padding: EdgeInsets.only(left: 20),
                          child: Container(
                            width: MediaQuery.of(context).size.width * 0.6,
                            child: Text(
                              'scan your receipts in seconds',
                              style: TextStyle(
                                fontFamily: 'Apercu',
                                fontSize: 20,
                                fontWeight: FontWeight.w500,
                                color: Color.fromARGB(255, 78, 80, 81),
                              ),
                            ),
                          ),
                        ),
                      ),
                      SizedBox(height: 70),
                      Align(
                        alignment: Alignment.bottomCenter,
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 20.0),
                          child: SizedBox(
                            width: MediaQuery.of(context).size.width * 0.9,
                            height: 50,
                            child: ElevatedButton(
                              onPressed: _loadImage,
                              style: ButtonStyle(
                                shape: MaterialStateProperty.all<
                                    RoundedRectangleBorder>(
                                  RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                                backgroundColor:
                                    MaterialStateProperty.all<Color>(
                                  Colors.black,
                                ),
                                minimumSize: MaterialStateProperty.all<Size>(
                                  Size(double.infinity, 60),
                                ),
                              ),
                              child: Container(
                                width: double.infinity,
                                child: Center(
                                  child: Text(
                                    'Take Photo',
                                    style: TextStyle(
                                      fontFamily: 'Apercu',
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              )
            : Container(
                height: MediaQuery.of(context).size.height,
                color: Colors.white,
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.file(
                          File(_capturedImage!.path),
                          width: MediaQuery.of(context).size.width * 0.8,
                        ),
                      ),
                      SizedBox(height: 20),
                      _processing
                          ? CircularProgressIndicator()
                          : Row(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              children: [
                                ElevatedButton(
                                  onPressed: _loadImage,
                                  style: ButtonStyle(
                                    backgroundColor:
                                        MaterialStateProperty.all<Color>(
                                            Colors.black),
                                  ),
                                  child: Text(
                                    'Retake Photo',
                                    style: TextStyle(
                                      fontFamily: 'OCRA',
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                                ElevatedButton(
                                  onPressed: _processImage,
                                  style: ButtonStyle(
                                    backgroundColor:
                                        MaterialStateProperty.all<Color>(
                                            Colors.black),
                                  ),
                                  child: Text(
                                    'Process Image',
                                    style: TextStyle(
                                      fontFamily: 'OCRA',
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                    ],
                  ),
                ),
              ),
      ),
    );
  }
}
