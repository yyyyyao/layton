#!/usr/bin/env ruby

################################################################################
# default
################################################################################
@file = "key_prob1.txt"

################################################################################
# Arguments
################################################################################
require "optparse"
OptionParser.new { |opts|
  # options
  opts.on("-h","--help","Show this message") {
    puts opts
    exit
  }
  opts.on("-i [INPUT]"){ |f|
    @file = f
  }
  # parse
  opts.parse!(ARGV)
}

################################################################################
# Class
################################################################################
########################################
# Array
########################################
class Array
  def sum
    self.inject(:+)
  end
end

########################################
# key
########################################
class MyKey
  #### new ####
  def initialize(file)
    @key = []
    open(file).read.split(/\n/).each do |line|
      @key.push(line.split.map{|i| i.to_i})
    end
    @sum = @key.inject(0){|sum, i| sum += i.sum} / 4
  end

  #### show ####
  def show(act)
    #### key ####
    for n in 0..@key.size-1
      for i in 0..3
        j = (i + act[n]) % 4
        printf("%3d", @key[n][j])
      end
      printf(" [%3d]\n", act[n])
    end

    #### sum ####
    for i in 0..3
      sum = 0
      for n in 0..@key.size-1
        j = (i + act[n]) % 4
        sum += @key[n][j]
      end
      printf("%3d", sum)
    end
    printf("\n")
  end

  #### test ####
  def test(act)
    for i in 0..3
      sum = 0
      for n in 0..@key.size-1
        j = (act[n] + i) % 4
        sum += @key[n][j]
      end
      return false if sum != @sum
    end
    true
  end

  #### successor of action ####
  def succ(act)
    for i in 1..@key.size
      j = @key.size - i
      act[j] += 1
      if act[j] == 4
        act[j] = 0
      else
        break
      end
    end
  end

  #### solver ####
  def solve
    act = Array.new(@key.size){|i| 0}
    while !test(act); succ(act); end
    show(act)
  end
end

################################################################################
# main
################################################################################
MyKey.new(@file).solve

