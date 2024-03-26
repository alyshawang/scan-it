import 'package:flutter/material.dart';
import 'package:receipt_scanner/process_image_page.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart' as firebase_storage;
import 'package:sliding_up_panel/sliding_up_panel.dart';

class ProcessedImagePage extends StatefulWidget {
  final String imageUrl;
  final double totalAmount;
  final String date;
  final String category;
  final Function resetCapturedImage;

  const ProcessedImagePage({
    Key? key,
    required this.imageUrl,
    required this.totalAmount,
    required this.date,
    required this.category,
    required this.resetCapturedImage,
  }) : super(key: key);

  @override
  _ProcessedImagePageState createState() => _ProcessedImagePageState();
}

class _ProcessedImagePageState extends State<ProcessedImagePage> {
  late String _selectedCategory;
  String _updatedDate = '';
  double _updatedTotalAmount = 0;

  @override
  void initState() {
    super.initState();
    _selectedCategory = widget.category;
    _updatedTotalAmount = widget.totalAmount;
    ;
    _updatedDate = widget.date;
  }

  Future<void> _uploadData() async {
    final Map<String, dynamic> payload = {
      'date': _updatedDate,
      'category': _selectedCategory,
      'total_amount': _updatedTotalAmount,
    };

    final jsonData = jsonEncode(payload);

    final url = 'http://192.168.2.17:5001/upload_data';
    final response = await http.post(
      Uri.parse(url),
      body: jsonData,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      print('Data uploaded successfully');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Stored to Excel')),
      );
      widget.resetCapturedImage();

      Navigator.pop(context);
    } else {
      print('Failed to upload data: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0.0,
        iconTheme: IconThemeData(color: Colors.black),
        actions: [
          IconButton(
            onPressed: _uploadData,
            icon: Icon(Icons.upload, color: Colors.black),
          ),
        ],
      ),
      body: SlidingUpPanel(
        minHeight: 250,
        maxHeight: MediaQuery.of(context).size.height * 0.5,
        panel: _buildPanel(),
        body: SingleChildScrollView(
          child: Column(
            children: [
              SizedBox(height: 20),
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.network(
                  widget.imageUrl,
                  width: MediaQuery.of(context).size.width * 0.9,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPanel() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: EdgeInsets.all(5),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    color: Color.fromRGBO(244, 243, 243, 1)),
                child: TextFormField(
                  initialValue: _updatedTotalAmount.toString(),
                  style: TextStyle(color: Color.fromARGB(255, 70, 70, 70)),
                  onChanged: (value) {
                    setState(() {
                      _updatedTotalAmount =
                          double.tryParse(value) ?? _updatedTotalAmount;
                    });
                  },
                  decoration: InputDecoration(
                    enabledBorder: InputBorder.none,
                    prefixIcon: Icon(Icons.attach_money),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Container(
                padding: EdgeInsets.all(5),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    color: Color.fromRGBO(244, 243, 243, 1)),
                child: TextFormField(
                  initialValue: _updatedDate,
                  style: TextStyle(color: Color.fromARGB(255, 70, 70, 70)),
                  onChanged: (value) {
                    setState(() {
                      _updatedDate = value;
                    });
                  },
                  decoration: InputDecoration(
                    enabledBorder: InputBorder.none,
                    prefixIcon: Icon(Icons.calendar_today),
                  ),
                ),
              ),
              SizedBox(height: 20),
              Text(
                'Category',
                style: TextStyle(
                  fontFamily: 'Manrope',
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 10),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: [
                  _buildCategoryButton('Groceries'),
                  _buildCategoryButton('Clothes'),
                  _buildCategoryButton('Office'),
                  _buildCategoryButton('Vehicle'),
                  _buildCategoryButton('Meals'),
                  _buildCategoryButton('Rent'),
                  _buildCategoryButton('Phone & Utilities'),
                  _buildCategoryButton('Supplies'),
                  _buildCategoryButton('Assets'),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCategoryButton(String category) {
    return ElevatedButton(
      onPressed: () {
        setState(() {
          _selectedCategory = category;
        });
      },
      style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all<Color>(
          _selectedCategory == category ? Colors.black : Colors.grey,
        ),
      ),
      child: Text(category),
    );
  }
}
