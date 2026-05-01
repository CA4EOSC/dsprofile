# Extending `dsprofile`

!!! info Developer-oriented Guide
    This section is intended for developers who wish to extend
    the functionality of `dsprofile` or include its features
    in their own projects.

## Overview

This section describes how to add functionality to `dsprofile`. This can
take two primary forms:

  1. Adding `Reader` support for additional dataset formats
  2. Adding `Writer` support for additional output formats

Guidelines are also provided to assist in integrating extensions to
`dsprofile` into its existing codebase, for example by providing
support for the command-line interface and unit-testing.

## Using `dsprofile` as a package

The `dsprofile` utility can be run as a standalone program, integrated
into workflow pipelines, invoked as a WSGI application, or included
directly within other Python programs.
