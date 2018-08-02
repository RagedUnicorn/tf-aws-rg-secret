output "public_key" {
  description = "Content of the generated private key"
  value       = "${data.external.generate_key_pair.result.public_key}"
}

output "key_name" {
  description = "The name of the key as it can be used in aws"
  value       = "${aws_key_pair.load_key_pair.key_name}"
}
