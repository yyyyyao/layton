#!/usr/bin/env ruby
# -*- coding: utf-8 -*-

################################################################################
# defualt
################################################################################
@@n = 3
@@show = false
@@one  = false

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
  opts.on("-n [INPUT]"){ |f|
    @@n = f.to_i
  }
  opts.on("-o", "--one"){ |f|
    @@one = true
    @@show = true
  }
  opts.on("-s", "--show"){ |f|
    @@show = true
  }
  # parse
  opts.parse!(ARGV)
}

################################################################################
# Array
################################################################################
class Array
  #### sum ####
  def sum
    self.inject(:+)
  end
  #### combination ####
  def combination(n)
    return [[]]              if n == 0
    return self.map{|i| [i]} if n == 1

    cs = []
    self.combination(n-1).each do |c|
      i = self.index(c.last)
      self[i+1..-1].each do |e|
        cs.push(c + [e])
      end
    end
    cs
  end
  #### permutation ####
  def permutation(n)
    return [[]]              if n == 0
    return self.map{|i| [i]} if n == 1

    ps = []
    self.permutation(n-1).each do |p|
      (self-p).each do |e|
        ps.push(p + [e])
      end
    end
    ps
  end
end

################################################################################
# main
################################################################################
# c1 b1 c2
# b3 C  b4
# c3 b2 c4

# Condition 1
# c1 - c2 = c3 - c4 := x1

# Condition 2
# c1 - c3 = c2 - c4 := x2

# Condition 3
# b2 - b1 = x2

# Condition 4
# b4 - b3 = x1

ns = Array.new(@@n**2){|i| i+1} # elements
num = 0                         # # solutions

#### Cores ####
ns.combination((@@n-2)**2).each do |core|
  edge = ns - core

  #### Coners ####
  # c1 - c2 = c3 - c4 := x1
  # c1 - c3 = c2 - c4 := x2
  edge.combination(4).each do |c|
    next if !( (c[0]-c[1] == c[2]-c[3]) && (c[0]-c[2] == c[1]-c[3]) )
    bar = edge - c
    x1 = c[0] - c[1]
    x2 = c[0] - c[2]

    #### Bar 1,2 ####8
    # b2 - b1 = x2
    bar.combination(@@n-2).each do |b1|
      (bar - b1).combination(@@n-2).each do |b2|
        next if !( b2.sum - b1.sum == x2)

        #### Bar 3,4 ####
        # b4 - b4 = x1
        (bar - b1 - b2).combination(@@n-2).each do |b3|
          b4 = bar - b1 - b2 - b3
          next if !(b4.sum - b3.sum == x1)
          puts "#{core}, #{c}, #{b1}, #{b2}, #{b3}, #{b4}" if @@show
          exit(1) if @@one
          num += 1
        end
      end
    end
  end
end

#### show # solutions ####
puts "# solutions = #{num}"
