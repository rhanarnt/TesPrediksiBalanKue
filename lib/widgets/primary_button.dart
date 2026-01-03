import 'package:flutter/material.dart';

class PrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool filled;

  const PrimaryButton(
      {super.key,
      required this.label,
      required this.onPressed,
      this.filled = true});

  @override
  Widget build(BuildContext context) {
    final bg = filled ? const Color(0xFFA855F7) : Colors.transparent;
    final fg = filled ? Colors.white : const Color(0xFFA855F7);
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: bg,
          foregroundColor: fg,
          elevation: 0,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
        onPressed: onPressed,
        child: Text(label,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
      ),
    );
  }
}
